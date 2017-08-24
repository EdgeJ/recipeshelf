class CreateRecipes < ActiveRecord::Migration[5.1]
  def change
    create_table :recipes do |t|
      t.string :title
      t.string :meal_type
      t.string :primary_ingredient
      t.integer :serving_size
      t.integer :amount
      t.text :body

      t.timestamps
    end
  end
end
