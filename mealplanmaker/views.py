from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Carbs, Drinks, Fats, Meals, Proteins, User, Weekly, Recipe, FoodIngredient




def index(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("weekly"))

    else:
        return render(request, "mealplanmaker/login.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mealplanmaker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mealplanmaker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

       
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mealplanmaker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mealplanmaker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mealplanmaker/register.html")

    
def mealcreation(request):

    if request.method == "GET":

        # Query that user's meals
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(mealcreator = request.user)
            no_user = False
        else:
            all_meals = None
            no_user = True

        context = {
            "all_meals": all_meals,
            "no_user": no_user
        }

        return render(request, "mealplanmaker/mealcreation.html", context)

    else:

        # Get inputs from form
        mealtitle = request.POST["mealtitle"]
        carb_source = request.POST.get("carbsource")
        carb_grams = request.POST.get("carbgrams")
        fat_source = request.POST.get("fatsource")
        fat_grams = request.POST.get("fatgrams")
        protein_source = request.POST.get("proteinsource")
        protein_grams = request.POST.get("proteingrams")
        drink_source = request.POST.get("drinksource")
        drinkmililiters = request.POST.get("drinkmililiters")
        

        
        if not carb_grams:
            carb_grams = 0
        if not fat_grams:
            fat_grams = 0
        if not protein_grams:
            protein_grams = 0
        if not drinkmililiters:
            drinkmililiters = 0
        #print(carb_grams)

        # Prepare variables to save in meal model
        mealcreator = request.user
        name = mealtitle

        # Get foods from models
        mealcarb = Carbs.objects.get(id=carb_source)
        mealfat = Fats.objects.get(id=fat_source)
        mealprotein = Proteins.objects.get(id=protein_source)
        mealdrink = Drinks.objects.get(id=drink_source)

        # Calculate total meal macros
        totalcarbs = round((int(getattr(mealcarb, "gcarb")) / 100 * int(carb_grams)) + (int(getattr(mealfat, "gcarb")) / 100 * int(fat_grams)) + (int(getattr(mealprotein, "gcarb")) / 100 * int(protein_grams)) + (int(getattr(mealdrink, "gcarb")) / 100 * int(drinkmililiters)))
        totalfats = round((int(getattr(mealcarb, "gfat")) / 100 * int(carb_grams)) + (int(getattr(mealfat, "gfat")) / 100 * int(fat_grams)) + (int(getattr(mealprotein, "gfat")) / 100 * int(protein_grams)) + (int(getattr(mealdrink, "gfat")) / 100 * int(drinkmililiters)))
        totalproteins = round((int(getattr(mealcarb, "gprotein")) / 100 * int(carb_grams)) + (int(getattr(mealfat, "gprotein")) / 100 * int(fat_grams)) + (int(getattr(mealprotein, "gprotein")) / 100 * int(protein_grams)) + (int(getattr(mealdrink, "gprotein")) / 100 * int(drinkmililiters)))
        #print(totalcarbs, totalfats, totalproteins)

        # Calculate total calories
        calories = (totalcarbs * 4) + (totalfats * 9) + (totalproteins * 4)
        #print(calories)

        # Make ingredients list
        carb_name = (getattr(mealcarb, "name"))
        fat_name = (getattr(mealfat, "name"))
        protein_name = (getattr(mealprotein, "name"))
        drink_name = (getattr(mealdrink, "name"))

        # Check for empty inputs
        if carb_name != "No Carb Source":
            there_is_carb = True
        else:
            there_is_carb = False
        if fat_name != "No Fat Source":
            there_is_fat = True
        else:
            there_is_fat = False
        if protein_name != "No Protein Source":
            there_is_protein = True
        else:
            there_is_protein = False
        if drink_name != "No Drink":
            there_is_drink = True
        else:
            there_is_drink = False

        # Format string quantity and macro name
        if there_is_carb:
            carb_ingredient = f'{carb_grams}g of {carb_name} '
        else:
            carb_ingredient = ""

        if there_is_fat:
            fat_ingredient = f'| {fat_grams}g of {fat_name} '
        else:
            fat_ingredient = ""

        if there_is_protein:
            protein_ingredient = f'| {protein_grams}g of {protein_name} '
        else:
            protein_ingredient = ""

        if there_is_drink:
            drink_ingredient = f'| {drinkmililiters}ml of {drink_name}'
        else:
            drink_ingredient = ""

        # Full ingredients list
        ingredients_list = f"{carb_ingredient}{fat_ingredient}{protein_ingredient}{drink_ingredient}"
        #print(ingredients_list)

        # Save meal
        meal = Meals(name = name, totalcarb = totalcarbs, totalfat = totalfats, totalprotein = totalproteins, calories = calories, mealcreator = mealcreator, ingredients = ingredients_list)
        meal.save()

        # Query that user's meals
        all_meals = Meals.objects.filter(mealcreator = request.user)
        

        context = {
            "all_meals": all_meals
        }

        return render(request, "mealplanmaker/mealcreation.html", context)

def deletemeal(request):

    
    all_meals = Meals.objects.filter(mealcreator = request.user)

    
    meal_id = request.POST.get("mealtodelete")
    meal_to_delete = Meals.objects.get(pk=meal_id)
    meal_to_delete.delete()

    context = {
        "all_meals": all_meals
    }

    return render(request, "mealplanmaker/mealcreation.html", context)

def weekly(request):

    user = request.user
    macros = {}
    percentage = {}

    if request.method == "GET":

        
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(mealcreator = user)
            weekly_meals = Weekly.objects.filter(mealuser = user)

            
            macros = calculate_macros(weekly_meals)
            percentage = calculate_percentage(macros)

            no_user = False
        else:
            all_meals = None
            weekly_meals = None
            macros = None
            percentage = None
            no_user = True

        context = {
            "all_meals": all_meals,
            "no_user": no_user,
            "weekly_meals": weekly_meals,
            "macros": macros,
            "percentage": percentage
        }

        return render(request, "mealplanmaker/weekly.html", context)

    else:

        # Query that user's meals
        if request.user.is_authenticated:
            all_meals = Meals.objects.filter(mealcreator = request.user)
            no_user = False
        else:
            all_meals = None
            no_user = True

        # Get form inputs for weekly model
        day = request.POST.get("day")
        meal_id = request.POST["meal_select"]
        meal_select = Meals.objects.get(pk = meal_id)
        user = request.user

        # Save weekly 
        weekly = Weekly(day = day, meal = meal_select, mealuser = user)
        weekly.save()

        weekly_meals = Weekly.objects.filter(mealuser = request.user)

        # Calculate Macros
        macros = calculate_macros(weekly_meals)
        percentage = calculate_percentage(macros)

        context = {
            "all_meals": all_meals,
            "no_user": no_user,
            "weekly_meals": weekly_meals,
            "macros": macros,
            "percentage": percentage
        }

        return render(request, "mealplanmaker/weekly.html", context)


def deletefromplan(request):

    # Find meal id and delete from Weekly object
    meal_id = request.POST.get("mealtodelete")
    meal_object = Meals.objects.get(pk = meal_id)
    daydelete = request.POST.get("daydelete")

    meal_to_delete = Weekly.objects.filter(meal = meal_object, mealuser = request.user, day = daydelete)
    object_to_delete = meal_to_delete.first()
    object_to_delete.delete()

    # Query that user's meals
    all_meals = Meals.objects.filter(mealcreator = request.user)
    weekly_meals = Weekly.objects.filter(mealuser = request.user)

    # Calculate Macros
    macros = calculate_macros(weekly_meals)
    percentage = calculate_percentage(macros)

    context = {
        "all_meals": all_meals,
        "monday_meals": all_meals,
        "weekly_meals": weekly_meals,
        "macros": macros,
        "percentage": percentage
    }

    return render(request, "mealplanmaker/weekly.html", context)

def calculate_macros(weekly_meals):

    weekly_fat = 0
    weekly_carb = 0
    weekly_protein = 0
    weekly_calories = 0

    for meal in weekly_meals:

        weekly_fat = weekly_fat + meal.meal.totalfat
        weekly_carb = weekly_carb + meal.meal.totalcarb
        weekly_protein = weekly_protein + meal.meal.totalprotein
        weekly_calories = weekly_calories + meal.meal.calories

    average_fat = round(weekly_fat / 7)
    average_carb = round(weekly_carb / 7)
    average_protein = round(weekly_protein / 7)
    average_calories = round(weekly_calories / 7)

    macros = {
        "average_fat": average_fat,
        "average_carb": average_carb,
        "average_protein": average_protein,
        "average_calories": average_calories,
    }

    return macros

def calculate_percentage(macros):

    calories_from_fat = macros.get("average_fat") * 9
    calories_from_carb = macros.get("average_carb") * 4
    calories_from_protein = macros.get("average_protein") * 4
    calories = macros.get("average_calories")

    if calories == 0:
        percentage = {
            "fat": 33,
            "carb": 33, 
            "protein": 33
        }

    else:
        fat = round((calories_from_fat / calories) * 100)
        carb = round((calories_from_carb / calories) * 100)
        protein = round((calories_from_protein / calories) * 100)
        
        percentage = {
            "fat": fat,
            "carb": carb, 
            "protein": protein
        }

    return percentage



def shelf(request):
    ingredients = FoodIngredient.objects.all()
    return render(request, "mealplanmaker/shelf.html", {'ingredients': ingredients})
    

  
def find_recipes(request):
    recipes = None
    missing_ingredients = []
    allergy_flagged_recipes = set()
    allergy_ingredient_names = {}
    all_ingredients = FoodIngredient.objects.filter(quantity__gt=Decimal('0.0'))

    if request.method == 'GET':
        ingredient_names = [name.strip().lower() for name in request.GET.get('ingr', '').split(',')]
        allergy_ingredients = [name.strip().lower() for name in request.GET.get('allergies', '').split(',')]

        if ingredient_names:
            found_ingredients = FoodIngredient.objects.filter(name__in=ingredient_names)
            found_ingredient_names = [ingredient.name.lower() for ingredient in found_ingredients]
            missing_ingredients = [name for name in ingredient_names if name not in found_ingredient_names]
            if not missing_ingredients:
                recipes = Recipe.objects.filter(FoodIngredient__in=found_ingredients).distinct()

        if allergy_ingredients:
            allergy_ingredients_objs = FoodIngredient.objects.filter(name__in=allergy_ingredients)
            allergy_recipes = Recipe.objects.filter(FoodIngredient__in=allergy_ingredients_objs).distinct()
            allergy_flagged_recipes = {recipe.id for recipe in allergy_recipes}

            # Populate the allergen names for flagged recipes
            for recipe in allergy_recipes:
                allergens = recipe.FoodIngredient.filter(name__in=allergy_ingredients).distinct()
                allergy_ingredient_names[recipe.id] = [allergen.name for allergen in allergens]

    return render(request, 'mealplanmaker/find_recipes.html', {
        'recipes': recipes,
        'missing_ingredients': missing_ingredients,
        'allergy_flagged_recipes': allergy_flagged_recipes,
        'allergy_ingredient_names': allergy_ingredient_names,
        'all_ingredients': all_ingredients,
    })
    
def make_ingredient_names_lowercase():
    ingredients = FoodIngredient.objects.all()
    for ingredient in ingredients:
        ingredient.name = ingredient.name.lower()
        ingredient.save()


make_ingredient_names_lowercase()
