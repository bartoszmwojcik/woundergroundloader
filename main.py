import logging
import argparse
from datetime import datetime, timedelta
from database import get_session, save_weather_data
from wunderground import WundergroundClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_date_range(start_date, end_date):
    """
    Validate the date range and provide warnings for large ranges
    Returns: (start_date, end_date, estimated_records)
    """
    if start_date > end_date:
        start_date, end_date = end_date, start_date
        logger.warning("Start date was after end date - dates have been swapped")
    
    date_range = (end_date - start_date).days
    estimated_records = date_range * 288  # Assuming 5-minute intervals
    estimated_size_mb = estimated_records * 100 / (1024 * 1024)  # Assuming 100 bytes per record
    
    logger.info(f"Date range: {date_range} days")
    logger.info(f"Estimated number of records: {estimated_records:,}")
    logger.info(f"Estimated storage needed: {estimated_size_mb:.2f} MB")
    
    if date_range > 365:
        logger.warning(f"Large date range detected ({date_range} days). This might take a while.")
    
    return start_date, end_date, estimated_records

def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid date format: {e}")

def main():
    """
    Main function to fetch and store historical weather data
    """
    parser = argparse.ArgumentParser(description='Fetch historical weather data from Weather Underground')
    parser.add_argument('--start-date', type=parse_date, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=parse_date, help='End date (YYYY-MM-DD)')
    parser.add_argument('--days', type=int, help='Number of days to fetch (from end date backwards)')
    args = parser.parse_args()

    # Set up date range
    end_date = args.end_date or datetime.now()
    if args.start_date:
        start_date = args.start_date
    elif args.days:
        start_date = end_date - timedelta(days=args.days)
    else:
        start_date = end_date - timedelta(days=30)  # Default to 30 days

    # Validate date range and get estimates
    start_date, end_date, estimated_records = validate_date_range(start_date, end_date)
    
    session = get_session()
    client = WundergroundClient()
    
    logger.info(f"Fetching historical weather data from {start_date.date()} to {end_date.date()}")
    
    # Counter for saved and skipped records
    saved_count = 0
    skipped_count = 0
    days_processed = 0
    last_progress_time = datetime.now()
    
    try:
        for weather_data in client.get_historical_data(start_date, end_date):
            if save_weather_data(session, weather_data):
                saved_count += 1
                
                # Show progress every 100 records or every 60 seconds
                current_time = datetime.now()
                if saved_count % 100 == 0 or (current_time - last_progress_time).seconds >= 60:
                    progress = (saved_count + skipped_count) / estimated_records * 100
                    logger.info(f"Progress: {progress:.1f}% - Saved: {saved_count:,} records, Skipped: {skipped_count:,} records")
                    last_progress_time = current_time
            else:
                skipped_count += 1
                
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user. Saving progress...")
    except Exception as e:
        logger.error(f"Error in main process: {e}")
    finally:
        total_records = saved_count + skipped_count
        logger.info(f"\nProcess completed:")
        logger.info(f"- Total records processed: {total_records:,}")
        logger.info(f"- New records saved: {saved_count:,}")
        logger.info(f"- Existing records skipped: {skipped_count:,}")
        if total_records > 0:
            logger.info(f"- Duplicate rate: {(skipped_count/total_records)*100:.1f}%")

if __name__ == "__main__":
    main() 