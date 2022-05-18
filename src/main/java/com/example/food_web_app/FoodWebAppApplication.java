package com.example.food_web_app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

import com.example.food_web_app.service.StorageProperties;

@SpringBootApplication
@EnableConfigurationProperties(StorageProperties.class)
public class FoodWebAppApplication {

    public static void main(String[] args) {
        SpringApplication.run(FoodWebAppApplication.class, args);
    }

}
