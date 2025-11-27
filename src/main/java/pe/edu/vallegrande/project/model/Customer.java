package pe.edu.vallegrande.project.model;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Entity
@Data
@Table(name = "customer", schema = "mas", uniqueConstraints = {
    @UniqueConstraint(columnNames = { "identification_document", "document_number" })
})
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false, updatable = false)
    private Long id;

    @NotBlank
    @Size(max = 50)
    @Column(name = "name", nullable = false, length = 50)
    private String name;

    @NotBlank
    @Size(max = 120)
    @Column(name = "last_name", nullable = false, length = 120)
    private String lastName;

    @Pattern(regexp = "9\\d{8}", message = "Debe empezar con 9 y tener 9 dígitos")
    @Column(name = "phone", length = 9)
    private String phone;

    @NotBlank
    @Email
    @Size(max = 120)
    @Column(name = "email", nullable = false, length = 120, unique = true)
    private String email;

    @NotBlank
    @Size(max = 120)
    @Column(name = "address", nullable = false, length = 120)
    private String address;

    @NotNull
    @Pattern(regexp = "DNI|CNE", message = "Solo se permite DNI o CNE")
    @Column(name = "identification_document", nullable = false, length = 3)
    private String identificationDocument;

    @NotBlank
    @Size(max = 15)
    @Column(name = "document_number", nullable = false, length = 15, unique = true)
    private String documentNumber;

    @Pattern(regexp = "A|I")
    @Column(name = "status", nullable = false, length = 1)
    private String status = "A";

    @Column(name = "registration_date", nullable = false)
    private LocalDate registrationDate = LocalDate.now();
}

