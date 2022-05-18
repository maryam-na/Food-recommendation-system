package com.example.food_web_app.model;

import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class FoodRequestDto {

    private MultipartFile[] photos;

    private List<String> fileNames;

    private boolean vegetarian;

    private List<String> meatTypes;

}
