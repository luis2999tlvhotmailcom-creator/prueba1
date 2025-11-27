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

import pe.edu.vallegrande.project.model.Seller;
import pe.edu.vallegrande.project.service.SellerService;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/v1/api/seller")
public class SellerRest {

    private final SellerService sellerService;

    public SellerRest(SellerService sellerService) {
        this.sellerService = sellerService;
    }

    @GetMapping
    public List<Seller> findAll() {
        return sellerService.findAll();
    }

    @GetMapping("/{id}")
    public Optional<Seller> findById(@PathVariable Long id) {
        return sellerService.findById(id);
    }

    @PostMapping("/save")
    public Seller save(@RequestBody Seller seller) {
        return sellerService.save(seller);
    }

    @PutMapping("/{id}")
    public Seller update(@PathVariable Integer id, @RequestBody Seller seller) {
        seller.setId(id);
        return sellerService.update(seller);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        sellerService.delete(id);
    }

    // Eliminado lógico (cambia status a "I")
    @DeleteMapping("/logical/{id}")
    public ResponseEntity<Void> logicalDelete(@PathVariable Long id) {
        Optional<Seller> sellerOpt = sellerService.findById(id);
        if (sellerOpt.isPresent()) {
            Seller seller = sellerOpt.get();
            seller.setStatus("I"); // inactivo
            sellerService.save(seller);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/restore/{id}")
    public ResponseEntity<Void> restore(@PathVariable Long id) {
        Optional<Seller> sellerOpt = sellerService.findById(id);
        if (sellerOpt.isPresent()) {
            Seller seller = sellerOpt.get();
            seller.setStatus("A");
            sellerService.save(seller);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
