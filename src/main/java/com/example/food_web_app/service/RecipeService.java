package com.example.food_web_app.service;

import java.util.*;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.webjars.NotFoundException;

import com.example.food_web_app.model.FoodRequestDto;
import com.example.food_web_app.model.Recipe;
import com.example.food_web_app.model.RecipeDto;
import com.example.food_web_app.repository.RecipeRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class RecipeService {

  private final RecipeRepository recipeRepository;

  private final RestTemplate restTemplate;

  public RecipeDto getRecipeDto(int recipeId) {
    Optional<Recipe> recipeOptional = recipeRepository.findById(recipeId);
    if (recipeOptional.isPresent()) {
      return RecipeDto.fromEntity(recipeOptional.get());
    }
    throw new NotFoundException("Recipe Not Found!");
  }

  public List<RecipeDto> getRecipesFromExternalService(FoodRequestDto foodRequestDto) {

    String uri = "http://localhost:5000/getRecipes";

    HttpHeaders headers = new HttpHeaders();
    headers.add("requestId", UUID.randomUUID().toString());

    HttpEntity<FoodRequestDto> httpEntity = new HttpEntity<>(foodRequestDto, headers);

    ResponseEntity<RecipeDto[]> response =
        restTemplate.exchange(uri, HttpMethod.POST, httpEntity, RecipeDto[].class);

    return Arrays.asList(Objects.requireNonNull(response.getBody()));

  }
}
