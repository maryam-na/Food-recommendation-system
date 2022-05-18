package com.example.food_web_app.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.food_web_app.model.RecipeDto;
import com.example.food_web_app.service.RecipeService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/recipe")
@RequiredArgsConstructor
public class RecipeController {

    private final RecipeService recipeService;

//    @GetMapping("/{recipeId}")
//    public RecipeDto getRecipe(@PathVariable int recipeId) {
//        return recipeService.getRecipeDto(recipeId);
//    }
}
