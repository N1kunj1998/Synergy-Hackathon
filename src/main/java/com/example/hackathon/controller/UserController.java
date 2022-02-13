package com.example.hackathon.controller;

import com.example.hackathon.model.User;
import com.example.hackathon.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
//@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    public ResponseEntity getPdf(){
        return ResponseEntity.ok("success");
    }

    @GetMapping("/user/{adhaarId}")
    public Optional<User> getUser (@PathVariable("adhaarId") String adhaarId){
        return userService.getUser(adhaarId);
    }

    @PostMapping("/user/{adhaarId}/{symptom}")
    public User setSymptom(@PathVariable("adhaarId") String adhaarId, @PathVariable("symptom")String symptom){
        return userService.setSymptom(adhaarId, symptom);
    }
}
