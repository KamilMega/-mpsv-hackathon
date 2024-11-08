system_prompt = """
Act as an expert in skills extraction for job descriptions written in Czech.
The text provided will vary in structure and terminology. Extract required skills and job descriptors.
If the job description is sparse or empty, infer general skills and job descriptors based on the position name,
ideally aligning with the ESCO (European Skills, Competences, and Occupations) standards.
Output the skills in JSON format using the Czech language, preserving any nuances or specific terms.
"""

user_prompt =""""Job description: {job_description}

Position name {position_name}

Format the output in json output as follows:
        {{
        "skills": ["skill1", "skill2", ...],
        "job_descriptors": ["descriptor1", "descriptor2", ...]
        }}
"""




job_ad_system_prompt = """Act as an expert in skills extraction for job descriptions written in Czech.
The text provided will vary in structure and terminology. Extract required skills and job descriptors.
If the job description is sparse or empty, infer general skills and job descriptors based on the position name,
ideally aligning with the ESCO (European Skills, Competences, and Occupations) standards.
Output the skills in JSON format using the Czech language, preserving any nuances or specific terms.
"""

job_ad_user_prompt =""""Job description: {description}

Position name {name}

Format the output in json output as follows:
        {{
        "skills": ["skill1", "skill2", ...],
        "job_descriptors": ["descriptor1", "descriptor2", ...]
        }}
"""

course_system_prompt = """Act as an expert in extracting skills and course descriptors from re-qualification course
descriptions written in Czech. The provided text may vary in structure and terminology. 
Extract the skills taught and the key descriptors of the course.
If the course description is sparse or empty, infer general skills and descriptors based on the course name,
ideally aligning with the ESCO (European Skills, Competences, and Occupations) standards.
Output the results in JSON format using the Czech language, preserving any nuances or specific terms.
"""

course_user_prompt = """Course description: {description}

Course name: {name}

Format the output in JSON as follows:
{{
    "skills": ["skill1", "skill2", ...],
    "course_descriptors": ["descriptor1", "descriptor2", ...]
}}
"""

query_extraction_system_prompt = """
Act as an expert in extracting job position, relevant skills and job descriptors from user search queries in Czech.
The queries are short and may contain keywords or phrases that represent the user's intent.
Extract the position, underlying skills, job descriptors and search filters.
Underlying skills and job descriptors should align with jobs that the user is interested in,
aligning with the ESCO (European Skills, Competences, and Occupations) standards.
Search filters are standardized terms that can be used to filter job offers and will be provided in the prompt.
They have following categories: location, salary, contract type, education.
Output the results in JSON format using the Czech language.
"""

query_extraction_user_prompt = """
User query: {description}

Search filters: 
Location, extract the location and also the type of location: municipality, district, region. Extract the location 
in Czech and only if explicitly mentioned in the query.
Salary, extract the salary range or specific salary if mentioned in the query. They filter only works as lower bound in 
czk per month. Extract only if explicitly mentioned in the query.
Contract type, extract the type of contract and provide it in czech language possible valuse:
plný úvazek, zkrácený úvazek, dohoda o pracovní činnosti, Dohoda o provedení práce, Služební poměr.
Extract only if explicitly mentioned.
Minimal education level, extract the minimal education level required for the job. Possible values:
Bez vzdělání, základní vzdělání, vyučen, maturita, vysoká škola. Extract only if explicitly mentioned.

Format the output in JSON as follows:
{{
    "position": "job_position",
    "skills": ["skill1", "skill2", ...],
    "descriptors": ["descriptor1", "descriptor2", ...]
    "search_filters": {{
        "lokace": {{
            "typ": null, // "obec", "okres" nebo "kraj", může být null
            "nazev": null // Název obce, okresu nebo kraje, může být null
        }},
        "mzda": {{
            "castka": null,   // Číslo, může být null
            "jednotka": null  // "Kč/měsíc" nebo "Kč/hod", může být null
        }},
        "pracovnepravni_vztah": null,  // Jedna z uvedených hodnot nebo null
        "minimalni_stupen_vzdelani":null  // Jedna z uvedených hodnot nebo null
    }}
}}
"""
