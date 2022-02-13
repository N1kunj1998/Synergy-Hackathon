package com.example.hackathon.service;

import com.example.hackathon.dao.UserRepository;
import com.example.hackathon.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {
    @Autowired
    private UserRepository repository;

    public String saveUser(User user){
        repository.save(user);
        return "user saved with Adhaar Id: " + user.getAdhaarId();
    }

    public User getDummyUser(){
//        UUID.randomUUID().toString(),
        return new User("741772380961","Nikunj","23/10/1998","Male","");
    }
    public Optional<User> getUser(String adhaarId){
        return repository.findById(adhaarId);
    }

    public User setSymptom(String adhaarId, String symptom){
        User user = repository.findById(adhaarId).orElse(new User());
        user.setSymptoms(symptom);
        repository.save(user);
        return user;
    }
}
