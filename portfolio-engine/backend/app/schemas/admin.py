from pydantic import BaseModel


class AdminOverviewResponse(BaseModel):
    total_portfolios: int
    total_projects: int
    total_featured_projects: int
    total_sections: int
    total_skills: int
    total_experiences: int
    total_education: int
    total_certifications: int
    total_social_links: int
    total_resumes: int
    total_project_media: int
    total_project_technologies: int
    total_users: int
