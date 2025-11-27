package pe.edu.vallegrande.project.service;

import java.util.List;
import java.util.Optional;
import pe.edu.vallegrande.project.model.Product;

public interface ProductService {

    List<Product> findAll();

    Optional<Product> findById(Integer id);

    Product save(Product product);

    Product update(Product product);

    void delete(Integer id);
}