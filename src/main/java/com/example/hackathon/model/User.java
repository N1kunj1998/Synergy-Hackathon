package com.example.hackathon.model;

import lombok.*;

import javax.persistence.*;
import java.io.Serializable;
import java.time.LocalTime;
import java.util.UUID;

@Entity
@Table
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class User implements Serializable {
//    @Id
//    @GeneratedValue
//    private String id;
//    @Column(unique = true)
    @Id
    private String adhaarId;
    private String name;
    private String DOB;
    private String gender;
    private String symptoms;
//    private LocalTime time;
}
