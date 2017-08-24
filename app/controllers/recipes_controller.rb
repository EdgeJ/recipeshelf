# Controller class for creating, updating, deleting recipes
class RecipesController < ApplicationController
  def index
    @recipes = Recipe.all
  end

  def new
    @recipe = Recipe.new
  end

  def edit
    @recipe = Recipe.find(params[:id])
  end

  def create
    @recipe = Recipe.new(recipe_params)

    if @recipe.save
      redirect_to @recipe
    else
      render 'new'
    end
  end

  def update
    @recipe = Recipe.find(params[:id])
    if @recipe.update(recipe_params)
      redirect_to @recipe
    else
      render 'edit'
    end
  end

  def show
    @recipe = Recipe.find(params[:id])
  end

  def delete
    # delete stuff
  end

  private

  def recipe_params
    params.require(:recipe).permit(
      :title,
      :meal_type,
      :primary_ingredient,
      :serving_size,
      :amount,
      :body
    )
  end
end
