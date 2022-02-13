package com.example.hackathon.controller;

import com.example.hackathon.helper.FileUploadHelper;
import com.example.hackathon.helper.PythonScriptRunner;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.io.File;

@RestController
public class FileUploadController {

    @Autowired
    private FileUploadHelper fileUploadHelper;
    @Autowired
    private PythonScriptRunner pythonScriptRunner;


    @PostMapping("/upload-file")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile multipartFile){
//        System.out.println(multipartFile.getOriginalFilename());
//        System.out.println(multipartFile.getSize());
//        System.out.println(multipartFile.getContentType());
//        System.out.println(multipartFile.getName());

        try {
            if (multipartFile.isEmpty()) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Request Must Contain file");
            }

            if (!multipartFile.getContentType().equals("image/jpeg")) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Only JPEG content type are allowed");
            }

            //File upload code
            boolean flag = fileUploadHelper.uploadFile(multipartFile);
            if(flag){
//                return ResponseEntity.ok("File is successfully uploaded");
                pythonScriptRunner.run(fileUploadHelper.UPLOAD_DIR + File.separator + multipartFile.getOriginalFilename());
//                return ResponseEntity.ok(ServletUriComponentsBuilder.fromCurrentContextPath().path("/image/").path(multipartFile.getOriginalFilename()).toUriString());
                return ResponseEntity.ok(pythonScriptRunner.adhaarId);
            }
        } catch (Exception e){
            e.printStackTrace();
        }

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Something went wrong! Try again");
    }
}
