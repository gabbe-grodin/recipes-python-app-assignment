from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


# CREATE
@app.route('/add/recipe/form')
def add_recipe_form():
    data = {"id": session["user_id"]}
    # is this the validation this needs?...
    if 'user_id' in session:
        User.get_one_user_by_id(data)
        return render_template('add_recipe.html')
    else:
        return redirect('/')

# create recipe "/add/recipe/submission"
@app.route('/add/recipe/submission', methods=['POST'])
def add_recipe():
    # trying to get value of radio button:
    # under_30 = request.form.get["under_30"]
    # needs validations like if user in session etc?
    Recipe.create_recipe(request.form)
    # under_30 = request.form.get("under_30")
    # return redirect('/dashboard', f"{under_30}")
    return redirect('/dashboard')

# show one recipe with user
@app.route("/view/recipe/<int:id>")
def show_one_recipe_with_creator(id):
    data = {"id": id}
    one_recipe = Recipe.get_one_recipe_by_id_with_creator(data)
    return render_template('view_recipe.html', recipe = one_recipe)

# edit recipe form
@app.route("/edit/recipe/<int:id>")
def edit_recipe_form(id):
    if 'user_id' not in session:
        return render_template('index.html')
    else:
        # to get prefilled data into edit form, select something (in this case a recipe or one_recipe) by id then pass into html
        data = {"id": id}
        one_recipe = Recipe.get_one_recipe_by_id_with_user(data)
        print(one_recipe)
        return render_template('edit_recipe.html', one_recipe = one_recipe)
    
# update recipe 
@app.route("/update/recipe/submission", methods=['POST'])
def update_recipe_submit():
    Recipe.update_one_recipe_by_id_with_user(request.form)
    return redirect(f"/view/recipe/{request.form['id']}")

# table of all recipes and their users
@app.route('/dashboard')
def show_all_recipes_with_users():
    logged_in_user = User.get_one_user_by_id(session['user_id'])
    if 'user_id' in session:
        all_recipes_with_users = Recipe.get_all_recipes_with_users()
        print(all_recipes_with_users)
        return render_template("dash.html", all_recipes = all_recipes_with_users, logged_in_user = logged_in_user)
    else:
        return redirect("/")
    
# delete one recipe 
@app.route("/delete/recipe/<int:id>") # needs to be a post?
def delete_one_recipe(id):
    data = {"id": id}
    Recipe.delete_one_recipe_by_id(data)
    return redirect('/dashboard')