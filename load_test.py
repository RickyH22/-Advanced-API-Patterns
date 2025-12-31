"""Load testing script"""
import asyncio
import httpx
import time
from statistics import mean, median

API_URL = "http://localhost:8000"
NUM_REQUESTS = 100
CONCURRENT_REQUESTS = 10

async def make_request(client, request_num):
    """Make a single request"""
    start = time.time()
    try:
        response = await client.get(f"{API_URL}/health")
        duration = time.time() - start
        return {
            "success": response.status_code == 200,
            "duration": duration,
            "status": response.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "duration": time.time() - start,
            "error": str(e)
        }

async def run_load_test():
    """Run load test"""
    print(f"Starting load test: {NUM_REQUESTS} requests with {CONCURRENT_REQUESTS} concurrent")
    print(f"Target: {API_URL}")
    print("-" * 60)
    
    results = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for batch in range(0, NUM_REQUESTS, CONCURRENT_REQUESTS):
            batch_size = min(CONCURRENT_REQUESTS, NUM_REQUESTS - batch)
            tasks = [make_request(client, i) for i in range(batch_size)]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            print(f"Completed {batch + batch_size}/{NUM_REQUESTS} requests")
    
    # Analyze results
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    durations = [r["duration"] for r in successful]
    
    print("\n" + "=" * 60)
    print("LOAD TEST RESULTS")
    print("=" * 60)
    print(f"Total Requests:     {len(results)}")
    print(f"Successful:         {len(successful)} ({len(successful)/len(results)*100:.1f}%)")
    print(f"Failed:             {len(failed)} ({len(failed)/len(results)*100:.1f}%)")
    
    if durations:
        print(f"\nResponse Times:")
        print(f"  Average:          {mean(durations):.3f}s")
        print(f"  Median:           {median(durations):.3f}s")
        print(f"  Min:              {min(durations):.3f}s")
        print(f"  Max:              {max(durations):.3f}s")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_load_test())
