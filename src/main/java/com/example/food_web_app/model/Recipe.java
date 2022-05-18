package com.example.food_web_app.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import javax.persistence.*;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "recipe", schema = "public")
public class Recipe {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String title;

    @OneToMany(mappedBy = "recipe", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Ingredient> ingredients;

    private String instructions;

    private String pictureLink;

    public static Recipe fromDto(RecipeDto recipeDto) {
        Recipe recipe = new Recipe();
        recipe.setTitle(recipeDto.getTitle());
        recipe.setInstructions(recipeDto.getInstructions());
        recipe.setPictureLink(recipeDto.getPictureLink());

        List<Ingredient> ingredientList = new ArrayList<>();

        if (Objects.nonNull(recipeDto.getIngredients())) {
            recipeDto.getIngredients().forEach(item -> {
                Ingredient ingredient = new Ingredient();
                ingredient.setName(item);
                ingredient.setRecipe(recipe);
                ingredientList.add(ingredient);
            });
        }

        recipe.setIngredients(ingredientList);
        return  recipe;
    }
}