"""Database seed script for Portfolio Engine.

Populates initial portfolio data for Yahaya Khalid, sample projects,
skills, experience, and an administrator account for local development.
"""

from datetime import date
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models import (
    Certification,
    Education,
    Experience,
    Portfolio,
    PortfolioSection,
    Project,
    ProjectMedia,
    ProjectTechnology,
    Resume,
    Skill,
    SocialLink,
    User,
)


def seed_database() -> None:
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Seed or retrieve superuser
        user = db.query(User).filter_by(email="developer@example.com").first()
        if not user:
            user = User(
                email="developer@example.com",
                hashed_password=hash_password("DevPassword123!"),
                full_name="Yahaya Khalid",
                is_active=True,
                is_superuser=True,
            )
            db.add(user)
            db.flush()
            print("✓ Created admin user: developer@example.com (Password: DevPassword123!)")
        else:
            print("• Admin user already exists")

        # 2. Seed Portfolio
        portfolio = db.query(Portfolio).filter_by(slug="khalid").first()
        if not portfolio:
            portfolio = Portfolio(
                name="Yahaya Khalid",
                slug="khalid",
                description="Senior Software Engineer & Systems Architect specializing in Python, FastAPI, distributed systems, and scalable backend engineering.",
            )
            db.add(portfolio)
            db.flush()
            print("✓ Created portfolio: Yahaya Khalid (slug: khalid)")
        else:
            print("• Portfolio 'khalid' already exists")

        portfolio_id = portfolio.id

        # 3. Seed Portfolio Sections
        if db.query(PortfolioSection).filter_by(portfolio_id=portfolio_id).count() == 0:
            sections = [
                PortfolioSection(
                    portfolio_id=portfolio_id,
                    title="About Me",
                    slug="about-me",
                    type="narrative",
                    content=(
                        "I am a backend engineer dedicated to building resilient, high-throughput systems "
                        "and maintainable architectures. With deep expertise in Python, asynchronous APIs, "
                        "relational data modeling, and cloud deployments, I focus on engineering solutions "
                        "that combine performance with clean design."
                    ),
                    position=1,
                    is_visible=True,
                ),
                PortfolioSection(
                    portfolio_id=portfolio_id,
                    title="Engineering Philosophy",
                    slug="engineering-philosophy",
                    type="narrative",
                    content=(
                        "Correctness over cleverness. Separation of concerns across data persistence, "
                        "domain business rules, and HTTP presentation. Automated test suites as contracts "
                        "for long-term maintainability."
                    ),
                    position=2,
                    is_visible=True,
                ),
            ]
            db.add_all(sections)
            db.flush()
            print(f"✓ Created {len(sections)} portfolio sections")

        # 4. Seed Projects
        if db.query(Project).filter_by(portfolio_id=portfolio_id).count() == 0:
            prj_engine = Project(
                portfolio_id=portfolio_id,
                title="Portfolio Engine",
                slug="portfolio-engine",
                description=(
                    "Long-term, content-driven personal portfolio API and administration system built with "
                    "FastAPI, PostgreSQL, SQLAlchemy 2.0, Argon2 authentication, and automated test coverage."
                ),
                github_url="https://github.com/Khaliddray/0x-engine",
                live_url="http://localhost:8000",
                is_featured=True,
            )
            prj_queue = Project(
                portfolio_id=portfolio_id,
                title="Distributed Event Pipeline",
                slug="distributed-event-pipeline",
                description=(
                    "Fault-tolerant asynchronous event queue engine with Redis and Python workers, "
                    "dead-letter queues, and real-time metric tracking."
                ),
                github_url="https://github.com/Khaliddray/distributed-event-pipeline",
                live_url="https://pipeline.example.com",
                is_featured=True,
            )
            prj_guard = Project(
                portfolio_id=portfolio_id,
                title="AuthGuard Zero-Trust Gateway",
                slug="authguard-gateway",
                description=(
                    "Microservice API gateway implementing Argon2 password hashing, scoped JWT token "
                    "authorization, and role-based access control."
                ),
                github_url="https://github.com/Khaliddray/authguard-gateway",
                live_url=None,
                is_featured=False,
            )
            db.add_all([prj_engine, prj_queue, prj_guard])
            db.flush()

            # Add Technologies to projects
            techs = [
                # Portfolio Engine
                ProjectTechnology(project_id=prj_engine.id, name="Python", slug="python", position=1),
                ProjectTechnology(project_id=prj_engine.id, name="FastAPI", slug="fastapi", position=2),
                ProjectTechnology(project_id=prj_engine.id, name="PostgreSQL", slug="postgresql", position=3),
                ProjectTechnology(project_id=prj_engine.id, name="SQLAlchemy", slug="sqlalchemy", position=4),
                ProjectTechnology(project_id=prj_engine.id, name="Alembic", slug="alembic", position=5),
                ProjectTechnology(project_id=prj_engine.id, name="Pytest", slug="pytest", position=6),
                # Distributed Queue
                ProjectTechnology(project_id=prj_queue.id, name="Python", slug="python", position=1),
                ProjectTechnology(project_id=prj_queue.id, name="Redis", slug="redis", position=2),
                ProjectTechnology(project_id=prj_queue.id, name="Docker", slug="docker", position=3),
                ProjectTechnology(project_id=prj_queue.id, name="Celery", slug="celery", position=4),
                # AuthGuard
                ProjectTechnology(project_id=prj_guard.id, name="Python", slug="python", position=1),
                ProjectTechnology(project_id=prj_guard.id, name="JWT", slug="jwt", position=2),
                ProjectTechnology(project_id=prj_guard.id, name="Argon2", slug="argon2", position=3),
            ]
            db.add_all(techs)

            # Add Media
            media = [
                ProjectMedia(
                    project_id=prj_engine.id,
                    url="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1000&auto=format&fit=crop&q=80",
                    alt_text="Portfolio Engine Architecture",
                    caption="Backend API Architecture and Schemas",
                    position=1,
                ),
                ProjectMedia(
                    project_id=prj_queue.id,
                    url="https://images.unsplash.com/photo-1518770660439-4636190af475?w=1000&auto=format&fit=crop&q=80",
                    alt_text="Distributed Systems Circuit",
                    caption="High-throughput message pipeline",
                    position=1,
                ),
            ]
            db.add_all(media)
            db.flush()
            print("✓ Created 3 projects with technologies and media")

        # 5. Seed Skills
        if db.query(Skill).filter_by(portfolio_id=portfolio_id).count() == 0:
            skills = [
                # Backend & Languages
                Skill(portfolio_id=portfolio_id, name="Python", slug="python", category="Languages", proficiency="Expert", position=1),
                Skill(portfolio_id=portfolio_id, name="FastAPI", slug="fastapi", category="Frameworks", proficiency="Expert", position=2),
                Skill(portfolio_id=portfolio_id, name="SQLAlchemy", slug="sqlalchemy", category="Frameworks", proficiency="Advanced", position=3),
                Skill(portfolio_id=portfolio_id, name="PostgreSQL", slug="postgresql", category="Databases", proficiency="Advanced", position=4),
                Skill(portfolio_id=portfolio_id, name="Redis", slug="redis", category="Databases", proficiency="Intermediate", position=5),
                Skill(portfolio_id=portfolio_id, name="Alembic", slug="alembic", category="Database Tooling", proficiency="Advanced", position=6),
                Skill(portfolio_id=portfolio_id, name="Docker", slug="docker", category="DevOps & Infrastructure", proficiency="Intermediate", position=7),
                Skill(portfolio_id=portfolio_id, name="Pytest & TDD", slug="pytest", category="Testing", proficiency="Advanced", position=8),
                Skill(portfolio_id=portfolio_id, name="RESTful Architecture", slug="rest-api", category="Architecture", proficiency="Expert", position=9),
            ]
            db.add_all(skills)
            db.flush()
            print(f"✓ Created {len(skills)} skills")

        # 6. Seed Experience
        if db.query(Experience).filter_by(portfolio_id=portfolio_id).count() == 0:
            experiences = [
                Experience(
                    portfolio_id=portfolio_id,
                    company="Engineering Solutions Ltd",
                    role="Senior Backend Architect",
                    employment_type="Full-time",
                    location="Remote",
                    start_date=date(2023, 1, 15),
                    end_date=None,
                    description="Architected distributed APIs, migration tooling, and asynchronous backend services handling millions of monthly requests with high reliability.",
                    position=1,
                    is_visible=True,
                ),
                Experience(
                    portfolio_id=portfolio_id,
                    company="Tech Systems Inc",
                    role="Backend Software Engineer",
                    employment_type="Full-time",
                    location="Hybrid",
                    start_date=date(2021, 6, 1),
                    end_date=date(2022, 12, 31),
                    description="Implemented RESTful microservices in Python, optimized database queries with SQLAlchemy and PostgreSQL, and integrated comprehensive automated testing.",
                    position=2,
                    is_visible=True,
                ),
            ]
            db.add_all(experiences)
            db.flush()
            print(f"✓ Created {len(experiences)} experiences")

        # 7. Seed Education
        if db.query(Education).filter_by(portfolio_id=portfolio_id).count() == 0:
            education = [
                Education(
                    portfolio_id=portfolio_id,
                    institution="University of Technology",
                    degree="Bachelor of Science",
                    field_of_study="Computer Science",
                    location="Nigeria",
                    start_date=date(2017, 9, 1),
                    end_date=date(2021, 5, 30),
                    description="Graduated with honors. Focused on Distributed Systems, Relational Database Theory, and Algorithms.",
                    position=1,
                    is_visible=True,
                )
            ]
            db.add_all(education)
            db.flush()
            print("✓ Created education history")

        # 8. Seed Certifications
        if db.query(Certification).filter_by(portfolio_id=portfolio_id).count() == 0:
            certs = [
                Certification(
                    portfolio_id=portfolio_id,
                    name="AWS Certified Solutions Architect – Associate",
                    issuer="Amazon Web Services",
                    credential_id="AWS-SA-2024-9102",
                    credential_url="https://aws.amazon.com/verification",
                    issue_date=date(2024, 2, 10),
                    description="Validation of distributed system design, cloud security, and high-availability architecture.",
                    position=1,
                    is_visible=True,
                ),
            ]
            db.add_all(certs)
            db.flush()
            print("✓ Created certifications")

        # 9. Seed Social Links
        if db.query(SocialLink).filter_by(portfolio_id=portfolio_id).count() == 0:
            links = [
                SocialLink(portfolio_id=portfolio_id, platform="GitHub", url="https://github.com/Khaliddray", label="github.com/Khaliddray", position=1, is_visible=True),
                SocialLink(portfolio_id=portfolio_id, platform="LinkedIn", url="https://linkedin.com/in/yahaya-khalid", label="LinkedIn Profile", position=2, is_visible=True),
                SocialLink(portfolio_id=portfolio_id, platform="Twitter", url="https://twitter.com/khaliddray", label="@khaliddray", position=3, is_visible=True),
                SocialLink(portfolio_id=portfolio_id, platform="Email", url="mailto:khalidzak21@gmail.com", label="khalidzak21@gmail.com", position=4, is_visible=True),
            ]
            db.add_all(links)
            db.flush()
            print(f"✓ Created {len(links)} social links")

        # 10. Seed Resume
        if db.query(Resume).filter_by(portfolio_id=portfolio_id).count() == 0:
            resume = Resume(
                portfolio_id=portfolio_id,
                title="Yahaya Khalid - Senior Backend Engineer CV",
                file_url="https://example.com/resumes/yahaya_khalid_cv.pdf",
                version="2026.1",
                description="Comprehensive engineering curriculum vitae highlighting technical skills, architectural projects, and career milestones.",
                is_primary=True,
                is_visible=True,
            )
            db.add(resume)
            db.flush()
            print("✓ Created primary resume reference")

        db.commit()
        print("\n Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
