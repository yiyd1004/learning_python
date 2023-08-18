from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


base_url = "https://www.indeed.com/jobs"
location_url = "l=Seattle%2C+WA&vjk=c56c5d0a21af45dc"


def get_page_count(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}?q={keyword}&{location_url}")

    soup = BeautifulSoup(browser.page_source.encode("utf-8"), "html.parser")
    h1 = soup.find("h1")
    if h1.text == u"This site can't be reached":
        print("Can't request website")
    else:
        pagination = soup.find("nav", {"aria-label": "pagination"})

        if pagination == None:
            return 1

        pages = pagination.find_all("div", recursive=False)
        count = len(pages)
        if count >= 5:
            return 5
        else:
            return count


def extract_indeed_jobs(keyword):
    print("Start fetching data from Indeed")
    results = []
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    for page in range(pages):
        final_url = f"{base_url}?q={keyword}&{location_url}&start={10 * page}"
        print("Requesting", final_url, "page", page)

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        browser = webdriver.Chrome(options=options)
        browser.get(final_url)

        soup = BeautifulSoup(
            browser.page_source.encode("utf-8"), "html.parser")
        h1 = soup.find("h1")
        if h1.text == u"This site can't be reached":
            print("Can't request website")
        else:
            zone = soup.find("div", id="mosaic-jobResults")

            if zone != None:
                job_list = zone.find("ul")
                jobs = job_list.find_all("li", recursive=False)
                for job in jobs:
                    anchor = job.select_one("h2 a")
                    if anchor != None:
                        title = anchor["aria-label"]
                        link = anchor["href"]
                        company = job.find("span", class_="companyName")
                        location = job.find("div", class_="companyLocation")

                        job_data = {
                            "link": f"https://www.indeed.com{link}",
                            "company": company.string.replace(",", " "),
                            "location": location.string.replace(",", " ") if location.string != None else "",
                            "position": title.replace(",", " ")
                        }
                        results.append(job_data)

    print("Finished fetching data from Indeed")
    return results
