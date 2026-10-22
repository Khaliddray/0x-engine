from app.models.portfolio import Portfolio
from app.models.project import Project
from app.models.user import User
from app.repositories.portfolio import PortfolioRepository
from app.repositories.project import ProjectRepository
from app.repositories.user import UserRepository


def test_portfolio_repository_crud(db):
    repo = PortfolioRepository(db)

    # 1. Create
    portfolio = Portfolio(
        name="Backend Portfolio",
        slug="backend-portfolio",
        description="Core systems",
    )
    created = repo.create(portfolio)
    assert created.id is not None
    assert created.slug == "backend-portfolio"

    # 2. Get by ID & Slug
    by_id = repo.get_by_id(created.id)
    assert by_id is not None
    assert by_id.name == "Backend Portfolio"

    by_slug = repo.get_by_slug("backend-portfolio")
    assert by_slug is not None
    assert by_slug.id == created.id

    # 3. Get all
    all_portfolios = repo.get_all()
    assert len(all_portfolios) == 1

    # 4. Update
    by_id.name = "Advanced Backend Portfolio"
    updated = repo.update(by_id)
    assert updated.name == "Advanced Backend Portfolio"

    # 5. Delete
    repo.delete(updated)
    assert repo.get_by_id(created.id) is None


def test_project_repository_crud(db):
    portfolio_repo = PortfolioRepository(db)
    project_repo = ProjectRepository(db)

    portfolio = portfolio_repo.create(
        Portfolio(name="Main", slug="main", description="Main portfolio")
    )

    # 1. Create project
    project = Project(
        portfolio_id=portfolio.id,
        title="Microservice Engine",
        slug="microservice-engine",
        description="High throughput API",
        is_featured=True,
    )
    created = project_repo.create(project)
    assert created.id is not None

    # 2. Get by portfolio ID
    projects = project_repo.get_by_portfolio_id(portfolio.id)
    assert len(projects) == 1
    assert projects[0].title == "Microservice Engine"

    # 3. Update
    created.is_featured = False
    updated = project_repo.update(created)
    assert updated.is_featured is False

    # 4. Delete
    project_repo.delete(updated)
    assert project_repo.get_by_id(created.id) is None


def test_user_repository_crud(db):
    repo = UserRepository(db)

    # 1. Create
    user = User(
        email="architect@example.com",
        hashed_password="hashed_placeholder_pwd",
        full_name="Software Architect",
        is_active=True,
        is_superuser=False,
    )
    created = repo.create(user)
    assert created.id is not None

    # 2. Get by email
    found = repo.get_by_email("architect@example.com")
    assert found is not None
    assert found.full_name == "Software Architect"

    # 3. Update
    found.is_active = False
    updated = repo.update(found)
    assert updated.is_active is False

    # 4. Delete
    repo.delete(updated)
    assert repo.get_by_email("architect@example.com") is None
