package pe.edu.vallegrande.project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pe.edu.vallegrande.project.model.Product;

public interface ProductRepository extends JpaRepository<Product, Integer> {
}