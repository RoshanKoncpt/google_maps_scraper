from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn
import os
import time
import sys

print("Starting Google Maps Scraper API...")
print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")

app = FastAPI(title="Google Maps Scraper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests and responses
class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 100
    visit_websites: Optional[bool] = True

class BusinessResult(BaseModel):
    name: str
    address: str
    rating: Optional[float]
    review_count: Optional[int]
    category: str
    website: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    secondary_email: Optional[str]
    google_maps_url: str
    search_query: str
    website_visited: bool
    additional_contacts: str

class SearchResponse(BaseModel):
    success: bool
    data: List[BusinessResult]
    total_results: int
    message: str

@app.get("/")
async def root():
    return {
        "message": "Google Maps Scraper API",
        "version": "1.0.0",
        "status": "active",
        "port": os.environ.get('PORT', 'NOT SET'),
        "endpoints": ["/", "/health", "/test-dependencies", "/test-chrome", "/test-google-maps", "/test-import", "/debug-scrape", "/debug-search", "/scrape"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "port": os.environ.get('PORT', 'NOT SET')
    }

@app.get("/test-dependencies")
async def test_dependencies():
    """Test if all Python dependencies are installed"""
    try:
        dependencies = {}

        # Test FastAPI
        try:
            import fastapi
            dependencies["fastapi"] = fastapi.__version__
        except ImportError as e:
            dependencies["fastapi"] = f"ERROR: {str(e)}"

        # Test Selenium
        try:
            import selenium
            dependencies["selenium"] = selenium.__version__
        except ImportError as e:
            dependencies["selenium"] = f"ERROR: {str(e)}"

        # Test other dependencies
        try:
            import uvicorn
            dependencies["uvicorn"] = uvicorn.__version__
        except ImportError as e:
            dependencies["uvicorn"] = f"ERROR: {str(e)}"

        try:
            import pydantic
            dependencies["pydantic"] = pydantic.__version__
        except ImportError as e:
            dependencies["pydantic"] = f"ERROR: {str(e)}"

        return {
            "status": "success",
            "dependencies": dependencies,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Dependency test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@app.get("/test-import")
async def test_import():
    """Test if we can import the optimized scraper"""
    try:
        print("🧪 Testing import of optimized_scraper...")

        # Try to import the optimized scraper
        from optimized_scraper import OptimizedGoogleMapsScraper

        # Try to create an instance
        scraper = OptimizedGoogleMapsScraper("test query", max_results=1)

        return {
            "status": "success",
            "message": "Successfully imported and instantiated OptimizedGoogleMapsScraper",
            "scraper_class": str(type(scraper)),
            "timestamp": datetime.now().isoformat()
        }

    except ImportError as e:
        return {
            "status": "error",
            "message": f"Import error: {str(e)}",
            "error_type": "ImportError",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"General error: {str(e)}",
            "error_type": type(e).__name__,
            "timestamp": datetime.now().isoformat()
        }

@app.get("/debug-scrape")
async def debug_scrape():
    """Debug the scraping process step by step"""
    try:
        print("🔍 Starting debug scrape with optimized scraper...")

        # Import the optimized scraper
        from optimized_scraper import OptimizedGoogleMapsScraper

        # Create scraper instance
        scraper = OptimizedGoogleMapsScraper("coffee shops in San Francisco", max_results=1)

        debug_info = {
            "step_1_import": "✅ Successfully imported scraper",
            "step_2_instance": "✅ Successfully created scraper instance",
            "step_3_browser_setup": "❌ Not attempted",
            "step_4_search": "❌ Not attempted",
            "step_5_links": "❌ Not attempted",
            "step_6_extraction": "❌ Not attempted",
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }

        # Test browser setup
        try:
            scraper.setup_browser()
            debug_info["step_3_browser_setup"] = "✅ Browser setup successful"

            # Test search
            try:
                search_result = scraper.search_google_maps()
                if search_result:
                    debug_info["step_4_search"] = "✅ Google Maps search successful"

                    # Test link extraction
                    try:
                        links = scraper.get_business_links()
                        debug_info["step_5_links"] = f"✅ Found {len(links)} business links"

                        if links:
                            # Test data extraction from first link
                            try:
                                data = scraper.extract_business_data(links[0])
                                if data and data.get('name') != 'Unknown Business':
                                    debug_info["step_6_extraction"] = f"✅ Successfully extracted: {data['name']}"
                                else:
                                    debug_info["step_6_extraction"] = "❌ Data extraction failed or returned empty"
                            except Exception as e:
                                debug_info["step_6_extraction"] = f"❌ Data extraction error: {str(e)}"
                                debug_info["errors"].append(f"Data extraction: {str(e)}")
                        else:
                            debug_info["step_5_links"] = "❌ No business links found"

                    except Exception as e:
                        debug_info["step_5_links"] = f"❌ Link extraction error: {str(e)}"
                        debug_info["errors"].append(f"Link extraction: {str(e)}")

                else:
                    debug_info["step_4_search"] = "❌ Google Maps search failed"

            except Exception as e:
                debug_info["step_4_search"] = f"❌ Search error: {str(e)}"
                debug_info["errors"].append(f"Search: {str(e)}")

        except Exception as e:
            debug_info["step_3_browser_setup"] = f"❌ Browser setup error: {str(e)}"
            debug_info["errors"].append(f"Browser setup: {str(e)}")

        finally:
            # Cleanup
            try:
                scraper.cleanup()
            except:
                pass

        return debug_info

    except Exception as e:
        return {
            "status": "error",
            "message": f"Debug error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/debug-search")
async def debug_search():
    """Debug Google Maps search in detail"""
    try:
        print("🔍 Starting detailed search debug with optimized scraper...")

        from optimized_scraper import OptimizedGoogleMapsScraper
        scraper = OptimizedGoogleMapsScraper("coffee shops in San Francisco", max_results=1)

        debug_info = {
            "browser_setup": "❌ Not attempted",
            "google_access": "❌ Not attempted",
            "maps_access": "❌ Not attempted",
            "search_attempt": "❌ Not attempted",
            "page_details": {},
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }

        # Setup browser
        try:
            scraper.setup_browser()
            debug_info["browser_setup"] = "✅ Browser setup successful"

            # Test basic Google access
            try:
                print("🌐 Testing basic Google access...")
                scraper.driver.get("https://www.google.com")
                time.sleep(3)

                google_title = scraper.driver.title
                google_url = scraper.driver.current_url

                debug_info["google_access"] = f"✅ Google accessible - Title: {google_title}"
                debug_info["page_details"]["google_title"] = google_title
                debug_info["page_details"]["google_url"] = google_url

                # Test Google Maps access
                try:
                    print("🗺️ Testing Google Maps access...")
                    scraper.driver.get("https://www.google.com/maps")
                    time.sleep(5)

                    maps_title = scraper.driver.title
                    maps_url = scraper.driver.current_url

                    debug_info["maps_access"] = f"✅ Maps accessible - Title: {maps_title}"
                    debug_info["page_details"]["maps_title"] = maps_title
                    debug_info["page_details"]["maps_url"] = maps_url

                    # Check for blocking indicators
                    page_source_snippet = scraper.driver.page_source[:500]
                    debug_info["page_details"]["page_source_snippet"] = page_source_snippet

                    if "sorry" in maps_title.lower() or "blocked" in page_source_snippet.lower():
                        debug_info["maps_access"] = f"❌ Maps blocked - Title: {maps_title}"
                        debug_info["errors"].append("Google Maps appears to be blocking access")

                    # Test search attempt
                    try:
                        print("🔍 Testing search functionality...")
                        search_result = scraper.search_google_maps()

                        if search_result:
                            debug_info["search_attempt"] = "✅ Search method returned True"

                            # Get final page details
                            final_title = scraper.driver.title
                            final_url = scraper.driver.current_url
                            debug_info["page_details"]["final_title"] = final_title
                            debug_info["page_details"]["final_url"] = final_url

                        else:
                            debug_info["search_attempt"] = "❌ Search method returned False"

                    except Exception as search_e:
                        debug_info["search_attempt"] = f"❌ Search error: {str(search_e)}"
                        debug_info["errors"].append(f"Search: {str(search_e)}")

                except Exception as maps_e:
                    debug_info["maps_access"] = f"❌ Maps access error: {str(maps_e)}"
                    debug_info["errors"].append(f"Maps access: {str(maps_e)}")

            except Exception as google_e:
                debug_info["google_access"] = f"❌ Google access error: {str(google_e)}"
                debug_info["errors"].append(f"Google access: {str(google_e)}")

        except Exception as browser_e:
            debug_info["browser_setup"] = f"❌ Browser error: {str(browser_e)}"
            debug_info["errors"].append(f"Browser: {str(browser_e)}")

        finally:
            try:
                scraper.cleanup()
            except:
                pass

        return debug_info

    except Exception as e:
        return {
            "status": "error",
            "message": f"Debug error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/test-chrome")
async def test_chrome():
    """Test if Chrome browser can be initialized"""
    try:
        print("🧪 Testing Chrome browser initialization...")

        # Try to import selenium
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            print("✅ Selenium imported successfully")
        except ImportError as e:
            return {
                "status": "error",
                "message": f"Selenium import failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

        # Enhanced Chrome options for Railway deployment
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--no-zygote")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-login-animations")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor,VizHitTestSurfaceLayer")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-dev-shm-usage")  # Critical for Docker
        chrome_options.add_argument("--disable-software-rasterizer")

        # Set Chrome binary location for Docker - try multiple paths
        import os
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser"
        ]

        chrome_binary = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_binary = path
                break

        if chrome_binary:
            chrome_options.binary_location = chrome_binary
            print(f"✅ Found Chrome binary at: {chrome_binary}")
        else:
            print("⚠️ No Chrome binary found, using system default")

        # Remove user data directory entirely - let Chrome handle it
        # This avoids the persistent directory conflict issue
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-update")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-web-resources")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--no-crash-upload")
        chrome_options.add_argument("--safebrowsing-disable-auto-update")
        chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")

        # Use memory-based approach instead of file system
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=4096")

        print("✅ Chrome options configured with unique user data directory")

        # Try to create driver with system Chrome only (avoid WebDriver Manager issues)
        try:
            # Use system Chrome directly
            driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome driver created successfully")

            # Simple test - just get the title without navigation
            driver.get("data:text/html,<html><head><title>Test Page</title></head><body>Test</body></html>")
            title = driver.title
            print(f"✅ Test page loaded: {title}")

            driver.quit()
            print("✅ Chrome driver closed successfully")

            return {
                "status": "success",
                "message": "Chrome browser working correctly on Railway",
                "method": "system-chrome",
                "test_page_title": title,
                "approach": "no-user-data-dir",
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Chrome test failed: {str(e)}")

            # No cleanup needed since we're not using temp directories

            return {
                "status": "error",
                "message": f"Chrome failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    except Exception as e:
        print(f"❌ Overall Chrome test failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Chrome test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@app.get("/test-google-maps")
async def test_google_maps_scraper():
    """Test Google Maps scraping functionality with a small sample"""
    try:
        print("🗺️ Testing Optimized Google Maps scraper...")

        # Import the optimized scraper class
        from optimized_scraper import optimized_scrape_google_maps

        # Run extraction with small test
        print("🚀 Starting optimized extraction process...")
        results = optimized_scrape_google_maps(
            query="coffee shops in San Francisco",
            max_results=3  # Small test
        )
        print(f"✅ Extraction completed. Results type: {type(results)}")

        if results and isinstance(results, list) and len(results) > 0:
            return {
                "status": "success",
                "message": f"Optimized Google Maps scraper working! Found {len(results)} businesses",
                "sample_count": len(results),
                "sample_data": results[:2] if len(results) >= 2 else results,  # Show first 2 results
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "partial_success",
                "message": "Optimized scraper initialized but no results found",
                "results": results,
                "timestamp": datetime.now().isoformat()
            }

    except Exception as e:
        print(f"❌ Google Maps scraper test failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Google Maps scraper failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ General error: {str(e)}")
        return {
            "status": "error",
            "message": f"Chrome test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@app.post("/scrape", response_model=SearchResponse)
async def scrape_google_maps(request: SearchRequest):
    """
    Main Google Maps scraping endpoint using optimized scraper
    """
    try:
        print(f"🔍 Received scraping request: {request.query}")
        print(f"📊 Max results: {request.max_results}")

        # Import the optimized scraper function
        from optimized_scraper import optimized_scrape_google_maps

        # Run extraction with optimized scraper
        print("🚀 Starting optimized extraction process...")
        results = optimized_scrape_google_maps(
            query=request.query,
            max_results=request.max_results
        )
        print(f"✅ Extraction completed. Found {len(results) if results else 0} results")

        if results and isinstance(results, list) and len(results) > 0:
            # Convert results to BusinessResult objects
            business_results = []
            for result in results:
                if isinstance(result, dict):
                    business_result = BusinessResult(
                        name=result.get('name', ''),
                        address=result.get('address', ''),
                        rating=result.get('rating'),
                        review_count=result.get('review_count'),
                        category=result.get('category', ''),
                        website=result.get('website'),
                        mobile=result.get('mobile'),
                        email=result.get('email'),
                        secondary_email=result.get('secondary_email'),
                        google_maps_url=result.get('google_maps_url', ''),
                        search_query=request.query,
                        website_visited=result.get('website_visited', False),
                        additional_contacts=result.get('additional_contacts', '')
                    )
                    business_results.append(business_result)

            return SearchResponse(
                success=True,
                data=business_results,
                total_results=len(business_results),
                message=f"Successfully scraped {len(business_results)} businesses"
            )
        else:
            return SearchResponse(
                success=False,
                data=[],
                total_results=0,
                message="No results found or extraction failed"
            )

    except Exception as e:
        print(f"❌ Scraping error: {str(e)}")
        error_msg = f"Scraping failed: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return SearchResponse(
            success=False,
            data=[],
            total_results=0,
            message=error_msg
        )


if __name__ == "__main__":
    # Get port from environment, default to 8000
    port = int(os.environ.get("PORT", 8000))

    print(f"🔍 Environment PORT: {os.environ.get('PORT', 'NOT SET')}")
    print(f"🌐 Starting server on 0.0.0.0:{port}")

    # Start the server
    uvicorn.run(app,host="0.0.0.0",port=port,log_level="info")
