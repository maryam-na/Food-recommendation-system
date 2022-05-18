package com.example.food_web_app.model;

import java.util.List;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class RecipeDto {

  private int id;

  private String title;

  private List<String> ingredients;

  private String instructions;

  @JsonProperty("picture_link")
  private String pictureLink;

  public static RecipeDto fromEntity(Recipe recipe) {
    RecipeDto recipeDto = new RecipeDto();
    recipeDto.setId(recipe.getId());
    recipeDto.setTitle(recipe.getTitle());
    recipeDto.setInstructions(recipe.getInstructions());
    recipeDto.setPictureLink(recipe.getPictureLink());
    recipeDto.setIngredients(
        recipe.getIngredients().stream().map(Ingredient::getName).collect(Collectors.toList()));
    return recipeDto;
  }
}
