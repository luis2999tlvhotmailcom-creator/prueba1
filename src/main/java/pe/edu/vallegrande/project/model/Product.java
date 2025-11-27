package pe.edu.vallegrande.project.model;

import java.math.BigDecimal;
import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Entity
@Data
@Table(name = "product", schema = "mas")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Oracle IDENTITY
    private Integer id;

    @NotBlank
    @Size(max = 50)
    @Column(nullable = false, length = 50)
    private String name;

    @Size(max = 30)
    @Column(length = 30)
    private String brand;

    @NotNull
    @DecimalMin(value = "0.00")
    @Digits(integer = 4, fraction = 2)
    @Column(name = "sales_price", nullable = false, precision = 6, scale = 2)
    private BigDecimal salesPrice;

    @NotNull
    @DecimalMin(value = "0.00")
    @Digits(integer = 4, fraction = 2)
    @Column(name = "purchase_price", nullable = false, precision = 6, scale = 2)
    private BigDecimal purchasePrice;

    @Size(max = 200)
    @Column(length = 200)
    private String description;

    @NotNull
    @Min(0)
    @Column(nullable = false)
    private Integer stock = 0; // default para Oracle

    @Column(name = "expiration_date")
    private LocalDate expirationDate;

    @NotNull
    @Pattern(regexp = "A|I")
    @Column(nullable = false, length = 1)
    private String status = "A"; // default para Oracle
}