# Controller class for creating, updating users and logging in.
class UsersController < ApplicationController
  def new
    @user = User.new
  end

  def edit
    @user = User.find(params[:username])
  end

  def create
    @user = User.new(User_params)

    if @user.save
      redirect_to 'recipeshelf#index'
    else
      render 'new'
    end
  end

  def update
    @user = User.find(params[:username])
    if @user.update(User_params)
      redirect_to @user
    else
      render 'edit'
    end
  end

  def show
    @user = User.find(params[:username])
  end

  def delete
    # delete stuff
  end

  private

  def user_params
    params.require(:user).permit(:username, :password)
  end
end
