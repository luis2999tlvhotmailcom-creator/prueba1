package pe.edu.vallegrande.project.rest;

import java.util.List;
import java.util.Optional;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import pe.edu.vallegrande.project.model.Product;
import pe.edu.vallegrande.project.service.ProductService;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/v1/api/product")
public class ProductRest {

    private final ProductService productService;

    public ProductRest(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public List<Product> findAll() {
        return productService.findAll();
    }

    @GetMapping("/{id}")
    public Optional<Product> findById(@PathVariable Integer id) {
        return productService.findById(id);
    }

    @PostMapping("/save")
    public Product save(@RequestBody Product product) {
        return productService.save(product);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Integer id, @RequestBody Product updateProduct) {
        // lógica de actualización
        return ResponseEntity.ok(updateProduct);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Integer id) {
        productService.delete(id);
    }

    @DeleteMapping("/logical/{id}")
    public ResponseEntity<Void> logicalDelete(@PathVariable Integer id) {
        Optional<Product> productOpt = productService.findById(id);
        if (productOpt.isPresent()) {
            Product product = productOpt.get();
            product.setStatus("I");
            productService.save(product);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/restore/{id}")
    public ResponseEntity<Void> restore(@PathVariable Integer id) {
        Optional<Product> productOpt = productService.findById(id);
        if (productOpt.isPresent()) {
            Product product = productOpt.get();
            product.setStatus("A");
            productService.save(product);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}