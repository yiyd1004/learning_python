from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    print("Start fetching data from WWR")
    base_url = "https://weworkremotely.com/remote-jobs/search?term="

    res = get(f"{base_url}{keyword}")

    results = []
    if res.status_code != 200:
        print("Can't request website: ", res.status_code)
    else:
        soup = BeautifulSoup(res.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all(
                "li", class_=lambda classes: classes and "view-all" not in classes)
            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[1]
                link = anchor["href"]
                company, kind, region = anchor.find_all(
                    "span", class_="company")
                title = anchor.find("span", class_="title")

                job_data = {
                    "link": f"https://weworkremotely.com{link}",
                    "company": company.string.replace(",", " "),
                    "location": region.string.replace(",", " "),
                    "position": title.string.replace(",", " ")
                }
                results.append(job_data)
    print("Finished fetching data from WWR")
    return results
