package com.example.hackathon.helper;

import com.example.hackathon.model.User;
import com.example.hackathon.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.UUID;

@Component
public class PythonScriptRunner {
    @Autowired
    private UserService userService;
    public String adhaarId;
    public boolean run(String imgPath) throws IOException {
//        String[] cmd ={
//                "python",
//                "/home/nikunj/Documents/tet.py",
//                imgPath
//        };
//        try {
//            Runtime.getRuntime().exec(cmd);
//        }catch (Exception e){
//            e.printStackTrace();
//        }
//        System.out.println("python script runner working");
        try {
            ProcessBuilder builder = new ProcessBuilder("python3",
                    "/home/nikunj/Documents/spring projects/hackathon/src/main/resources/python-script/hackathon_synergy.py",
                     imgPath);
            Process process = builder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedReader readers = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String lines = null;
            ArrayList<String> data = new ArrayList<String>();
            while((lines= reader.readLine()) != null){
                System.out.println("lines: " + lines);
                data.add(lines);
            }
//            UUID.randomUUID().toString(),
            if(data.size() <=4){
                User user = new User(
                        (0 < data.size() ? data.get(0) : ""),
                        (2 < data.size() ? data.get(2) : ""),
                        (1 < data.size() ? data.get(1) : ""),
                        (3 < data.size() ? data.get(3) : ""),
                        "");
                userService.saveUser(user);
                adhaarId = data.get(0);
            } else {
                return false;
            }
            lines = null;
            while((lines= readers.readLine()) != null){
                System.out.println("lines: " + lines);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
        return true;
    }
}
