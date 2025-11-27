package pe.edu.vallegrande.project.service.impl;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

import lombok.extern.slf4j.Slf4j;
import pe.edu.vallegrande.project.model.Product;
import pe.edu.vallegrande.project.repository.ProductRepository;
import pe.edu.vallegrande.project.service.ProductService;

@Slf4j
@Service
public class ProductServiceImpl implements ProductService {

    private final ProductRepository productRepository;

    
    public ProductServiceImpl(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Override
    public List<Product> findAll() {
        log.info("Listando productos");
        return productRepository.findAll();
    }

    @Override
    public Optional<Product> findById(Integer id) {
        log.info("Buscando producto por ID: {}", id);
        return productRepository.findById(id);
    }

    @Override
    public Product save(Product product) {
        log.info("Registrando producto: {}", product);
        return productRepository.save(product);
    }

    @Override
    public Product update(Product product) {
        log.info("Actualizando producto: {}", product);
        return productRepository.save(product);
    }

    @Override
    public void delete(Integer id) {
        log.info("Eliminando producto con ID: {}", id);
        productRepository.deleteById(id);
    }
}