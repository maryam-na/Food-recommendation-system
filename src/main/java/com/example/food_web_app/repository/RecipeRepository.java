package com.example.food_web_app.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.food_web_app.model.Recipe;

@Repository
public interface RecipeRepository extends JpaRepository<Recipe, Integer> {

}
