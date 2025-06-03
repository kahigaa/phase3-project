
import typer
from datetime import date
from typing import Optional
from myapp.db.database import SessionLocal
from myapp.controllers import (
    user_controller,
    foodentry_controller,
    goal_controller,
    meal_controller,
)
import json
from typing import Optional

from myapp.models.meal_plan import MealPlan
app = typer.Typer()

# Subcommand grp
user_app = typer.Typer()
entry_app = typer.Typer()
goal_app = typer.Typer()
meal_plan_app = typer.Typer()
report_app = typer.Typer()


# User comds
@user_app.command("create")
def create_user(
    name: str = typer.Option(..., "--name", help="Name of the user")
):
    """Create a new user."""
    with SessionLocal() as session:
        user = user_controller.create_user(session, name)
        typer.echo(f"✅ User created: {user.name} (ID: {user.id})")

@user_app.command("list")
def list_users():
    """List all users."""
    with SessionLocal() as session:
        users = user_controller.list_users(session)
        for u in users:
            typer.echo(f"{u.id}: {u.name}")


# entry comds
@entry_app.command("add")
def add_entry(
    user: str = typer.Option(..., "--user", help="Name of the user"),
    food: str = typer.Option(..., "--food", help="Name of the food"),
    calories: int = typer.Option(..., "--calories", help="Calories in the food"),
    entry_date: str = typer.Option(..., "--date", help="Date of the entry (YYYY-MM-DD)")
):
    """Add a food entry."""
    with SessionLocal() as session:
        user_obj = user_controller.get_user_by_name(session, user)
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            raise typer.Exit(code=1)
        parsed_date = date.fromisoformat(entry_date)
        entry = foodentry_controller.add_food_entry(session, user_obj.id, food, calories, parsed_date)
        typer.echo(f"✅ Entry added: {entry.food} ({entry.calories} cal) on {entry.date}")

@entry_app.command("list")
def list_entries(
    user: str = typer.Option(..., "--user", help="Name of the user"),
    entry_date: str = typer.Option(..., "--entry-date", help="Date of the entry (YYYY-MM-DD)")
):
    """List food entries for a user on a specific date."""
    with SessionLocal() as session:
        user_obj = user_controller.get_user_by_name(session, user)
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            raise typer.Exit(code=1)
        d = date.fromisoformat(entry_date)
        entries = foodentry_controller.list_food_entries(session, 
        user_obj.id, d)
        for e in entries:
            typer.echo(f"{e.id}: {e.food} - {e.calories} cal on {e.date}")

@entry_app.command("update")
def update_entry(
    id: int = typer.Option(..., "--id", help="ID of the food entry to update"),
    food: Optional[str] = typer.Option(None, "--food", help="Updated name of the food"),
    calories: Optional[int] = typer.Option(None, "--calories", help="Updated calories"),
    entry_date: Optional[str] = typer.Option(None, "--entry-date", help="Updated date (YYYY-MM-DD)")
):
    with SessionLocal() as session:
        updated = foodentry_controller.update_food_entry(session, id, food, calories, entry_date)
        if updated:
            typer.echo("✅ Entry updated")
        else:
            typer.echo("⚠️ Entry not found")

@entry_app.command("delete")
def delete_entry(id: int = typer.Option(..., "--id", help="ID of the food entry to delete")):
    with SessionLocal() as session:
        success = foodentry_controller.delete_food_entry(session, id)
        if success:
            typer.echo(f"🗑️ Entry with ID {id} deleted.")
        else:
            typer.echo(f"⚠️ Entry with ID {id} not found.")


#goal comds
@goal_app.command("set")
def set_goal(
    user: str = typer.Option(..., "--user", help="Name of the user"),
    daily: int = typer.Option(..., "--daily", help="Daily calorie goal"),
    weekly: int = typer.Option(..., "--weekly", help="Weekly calorie goal")
):
    with SessionLocal() as session:

        user_obj = user_controller.get_user_by_name(session, user)
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            raise typer.Exit(code=1)

        goal = goal_controller.set_goal(session, user_obj.id, daily, weekly)
        typer.echo(f"🎯 Goal set for {user}: {goal.daily}/day, {goal.weekly}/week")


@goal_app.command("list")
def list_goals(
    user: str = typer.Option(..., "--user", help="Name of the user")
):
    with SessionLocal() as session:
    
        user_obj = user_controller.get_user_by_name(session, user)
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            raise typer.Exit(code=1)

    
        goals = goal_controller.list_goals(session, user_obj.id)
        if not goals:
            typer.echo(f"⚠️ No goals found for user '{user}'.")
            return
        for g in goals:
            typer.echo(f"🎯 Goal ID {g.id}: {g.daily}/day, {g.weekly}/week")


# meal plan commands 
@meal_plan_app.command("create")
def create_meal_plan(
    user: str = typer.Option(..., "--user", help="Name of the user"),
    week: int = typer.Option(..., "--week", help="Week number for the meal plan"),
    meals: str = typer.Option(..., "--meals", help="Planned meals in JSON format")
):
    with SessionLocal() as session:
        user_obj = user_controller.get_user_by_name(session, user)
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            raise typer.Exit(code=1)

        try:
            meals_data = json.loads(meals)  
        except json.JSONDecodeError:
            typer.echo("❌ Invalid JSON format for meals.")
            raise typer.Exit(code=1)

        plan = meal_controller.create_meal_plan(session, user_obj.id, week, meals_data)
        typer.echo(f"📅 Meal plan for week {plan.week} created for user '{user}' with meals: {plan.meals}.")

@meal_plan_app.command("update")
def update_meal_plan(
    id: int = typer.Option(..., "--id", help="ID of the meal plan to update"),
    week: Optional[int] = typer.Option(None, "--week", help="Updated week number"),
    meals: Optional[str] = typer.Option(None, "--meals", help="Updated meals in JSON format")
):
    with SessionLocal() as session:
        meals_data = None
        if meals:
            try:
                meals_data = json.loads(meals)  
            except json.JSONDecodeError:
                typer.echo("❌ Invalid JSON format for meals.")
                raise typer.Exit(code=1)

        updated = meal_controller.update_meal_plan(session, id, week, meals_data)
        if updated:
            typer.echo(f"🔁 Meal plan with ID {id} updated.")
        else:
            typer.echo(f"⚠️ Meal plan with ID {id} not found.")
@meal_plan_app.command("list")
def list_meal_plans(
    user: Optional[str] = typer.Option(None, "--user", help="Name of the user")
):
    
    with SessionLocal() as session:
        if user:
            user_obj = user_controller.get_user_by_name(session, user)
            if not user_obj:
                typer.echo(f"❌ User '{user}' not found.")
                raise typer.Exit(code=1)
            meal_plans = session.query(MealPlan).filter(MealPlan.user_id == user_obj.id).all()
        else:
            meal_plans = session.query(MealPlan).all()

        if not meal_plans:
            typer.echo("📭 No meal plans found.")
            return

        typer.echo("📋 Meal Plans:")
        for plan in meal_plans:
            typer.echo(f"- ID: {plan.id}, User ID: {plan.user_id}, Week: {plan.week}, Meals: {plan.meals}")

#report commands 
@report_app.command("daily")
def daily_report(
    user: str = typer.Option(..., "--user", help="User name"),
    report_date: str = typer.Option(..., "--date", help="Date of the report (YYYY-MM-DD)")
):
    with SessionLocal() as session:
        user_obj = user_controller.get_user_by_name(session, user)
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            raise typer.Exit(code=1)

        try:
            d = date.fromisoformat(report_date)
        except ValueError:
            typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
            raise typer.Exit(code=1)

        entries = foodentry_controller.list_food_entries(session, user_id=user_obj.id, entry_date=d)
        total_calories = sum(e.calories for e in entries)

        goals = goal_controller.list_goals(session, user_obj.id)
        daily_goal = goals[-1].daily if goals else None
        
        typer.echo(f"📅 Report for {report_date}:")
        typer.echo(f"- Total Calories Consumed: {total_calories} cal")
        if daily_goal is not None:
            typer.echo(f"- Daily Goal: {daily_goal} cal")
        else:
            typer.echo("- Daily Goal: Not set")        
        if entries:
            typer.echo("\nEntries:")
            for e in entries:
                typer.echo(f"  - {e.food}: {e.calories} cal")
        else:
            typer.echo("\nNo entries found for this day.")


# register subcommands 
app.add_typer(user_app, name="user")
app.add_typer(entry_app, name="entry")
app.add_typer(goal_app, name="goal")
app.add_typer(meal_plan_app, name="plan-meal")
app.add_typer(report_app, name="report")



if __name__ == "__main__":
    app()
