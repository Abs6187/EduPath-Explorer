import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://courses.analyticsvidhya.com/collections?page="
course_url_base = "https://courses.analyticsvidhya.com"

course_data = []

for page in range(1,9):
    print(f"Scraping page {page}...")
    response = requests.get(base_url + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    course_section = soup.find_all('div', class_="collections__product-cards collections__product-cards___0b9ab")
    if not course_section:
        print("No course section found, skipping this page.")
        continue
    
    courses = course_section[0].find_all('li')
    
    for course in courses:
        link_tag = course.find('a', href=True)
        if not link_tag:
            continue
        course_relative_link = link_tag['href']
        course_link = course_url_base + course_relative_link
        
        course_response = requests.get(course_link)
        course_soup = BeautifulSoup(course_response.text, 'html.parser')
        
        title_tag = course_soup.find('h1', class_="section__heading")
        if title_tag:
            course_title = title_tag.get_text(strip=True)
        else:
            course_title = "N/A"
        
        description_tag = course_soup.find_all('div', class_="rich-text__container")
        course_description = " ".join([p.get_text(strip=True) for tag in description_tag for p in tag.find_all('p')]) if description_tag else "N/A"
        
        curriculum_section = course_soup.find('div', class_="course-curriculum__container")
        if curriculum_section:
            curriculum_content = []
            
            chapters = curriculum_section.find_all('li', class_="course-curriculum__chapter")
            for chapter in chapters:
                title = chapter.find('h5', class_="course-curriculum__chapter-title")
                if title:
                    curriculum_content.append(title.get_text(strip=True))
                    
                    chapter_content = chapter.find('ul', class_="course-curriculum__chapter-content")
                    if chapter_content:
                        curriculum_content.extend(
                            [f"  - {item.get_text(strip=True)}" for item in chapter_content.find_all('li')]
                        )
            course_curriculum = "\n".join(curriculum_content) if curriculum_content else "N/A"
        else:
            course_curriculum = "N/A"
        
        course_data.append({
            "Course Title": course_title,
            "Course Description": course_description,
            "Course Curriculum": course_curriculum,
            "Link": course_link
        })
        
        time.sleep(1)

df = pd.DataFrame(course_data)
file_path = r"C:\Users\rachi\OneDrive\Desktop\Analytics VIdya - Gen AI\analytics_vidhya_courses.xlsx"
df.to_excel(file_path, index=False)
print(f"Data saved to {file_path}")
