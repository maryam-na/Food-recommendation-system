package com.example.food_web_app.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.example.food_web_app.model.FoodRequestDto;
import com.example.food_web_app.model.RecipeDto;
import com.example.food_web_app.service.FileSystemStorageService;
import com.example.food_web_app.service.RecipeService;

import lombok.RequiredArgsConstructor;

@Controller
@RequestMapping("/food")
@RequiredArgsConstructor
public class FoodController {

  private final FileSystemStorageService fileSystemStorageService;

  private final RecipeService recipeService;

  @GetMapping("/recipe/{recipeId}")
  public String getRecipeDetails(@PathVariable int recipeId, Model model) {
    RecipeDto recipeDto = recipeService.getRecipeDto(recipeId);
    model.addAttribute("recipe", recipeDto);
    return "recipeDetails.html";
  }

  @GetMapping("new")
  public String getFoodDetails(Model model) {
    FoodRequestDto foodRequestDto = new FoodRequestDto();
    model.addAttribute("foodRequestDto", foodRequestDto);
    model.addAttribute("allMeatTypes", List.of("Red meat", "Poultry", "Sea food"));
    return "new.html";
  }

  @PostMapping("new")
  public String postFoodDetails(
      FoodRequestDto foodRequestDto, BindingResult bindingResult, Model model) {

    String folderName = fileSystemStorageService.createFolder();

    ArrayList<String> fileNames =
        fileSystemStorageService.storeMultiple(foodRequestDto.getPhotos(), "upload_", folderName);
    foodRequestDto.setFolderName(folderName);
    foodRequestDto.setFileNames(fileNames);
    foodRequestDto.setPhotos(null);

    List<RecipeDto> recipes = recipeService.getRecipesFromExternalService(foodRequestDto);
    model.addAttribute("recipes", recipes);
    return "recipeList.html";
  }
}
