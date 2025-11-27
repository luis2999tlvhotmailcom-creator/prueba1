package pe.edu.vallegrande.project.model;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Entity
@Data
@Table(name = "supplier")
public class Supplier {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id;

    @NotBlank
    @Size(max = 50)
    @Column(name = "name", nullable = false, length = 50)
    private String name;

    @NotBlank
    @Pattern(regexp = "1\\d{10}|2\\d{10}", message = "El RUC debe iniciar con 1 o 2 y tener 11 dígitos.")
    @Column(name = "ruc", nullable = false, unique = true, length = 11)
    private String ruc;

    @NotBlank
    @Column(name = "tipo_empresa")
    private String tipoEmpresa;

    @NotBlank
    @Pattern(regexp = "9\\d{8}", message = "El teléfono debe iniciar con 9 y tener 9 dígitos.")
    @Column(name = "phone", nullable = false, length = 9)
    private String phone;

    @NotBlank
    @Email
    @Size(max = 120)
    @Column(name = "email", nullable = false, unique = true, length = 120)
    private String email;

    @Size(max = 150)
    @Column(name = "address", length = 150)
    private String address;

    @Size(max = 50)
    @Column(name = "contact_name", length = 50)
    private String contactName;

    @Pattern(regexp = "9\\d{8}", message = "El teléfono de contacto debe iniciar con 9 y tener 9 dígitos.")
    @Column(name = "contact_phone", length = 9)
    private String contactPhone;

    @Email
    @Size(max = 150)
    @Column(name = "contact_email", length = 150)
    private String contactEmail;

    @Pattern(regexp = "A|I", message = "El estado debe ser A (Activo) o I (Inactivo).")
    @Column(name = "status", nullable = false, length = 1) // ✅ Permitimos inserción y actualización
    private String status;

    @Column(name = "registration_date", nullable = false) // ✅ Permitimos inserción y actualización
    private LocalDate registrationDate;
}