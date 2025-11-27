package pe.edu.vallegrande.project.rest;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import pe.edu.vallegrande.project.model.Supplier;
import pe.edu.vallegrande.project.service.SupplierService;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/v1/api/supplier")
public class SupplierRest {

    private final SupplierService supplierService;

    public SupplierRest(SupplierService supplierService) {
        this.supplierService = supplierService;
    }

    @GetMapping
    public List<Supplier> findAll() {
        return supplierService.findAll();
    }

    @GetMapping("/{id}")
    public Optional<Supplier> findById(@PathVariable Integer id) {
        return supplierService.findById(id);
    }

    @PostMapping("/save")
    public ResponseEntity<Supplier> save(@RequestBody Supplier supplier) {
        System.out.println("📦 Datos recibidos del frontend:");
        System.out.println(supplier); // <-- Esto imprime todos los valores del proveedor

        if (supplier.getStatus() == null) {
            supplier.setStatus("A");
        }
        if (supplier.getRegistrationDate() == null) {
            supplier.setRegistrationDate(LocalDate.now());
        }

        Supplier savedSupplier = supplierService.save(supplier);
        return ResponseEntity.ok(savedSupplier);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Supplier> updateSupplier(@PathVariable Integer id, @RequestBody Supplier updatedSupplier) {
        Optional<Supplier> optional = supplierService.findById(id);
        if (optional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
    
        Supplier existing = optional.get();
    
        // Campos permitidos
        existing.setName(updatedSupplier.getName());
        existing.setRuc(updatedSupplier.getRuc());
        existing.setPhone(updatedSupplier.getPhone());
        existing.setEmail(updatedSupplier.getEmail());
        existing.setAddress(updatedSupplier.getAddress());
        existing.setContactName(updatedSupplier.getContactName());
        existing.setContactPhone(updatedSupplier.getContactPhone());
        existing.setContactEmail(updatedSupplier.getContactEmail());
        existing.setTipoEmpresa(updatedSupplier.getTipoEmpresa());
    
        Supplier saved = supplierService.save(existing);
        return ResponseEntity.ok(saved);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Integer id) {
        supplierService.delete(id);
    }

    @PatchMapping("/logical/{id}")
    public ResponseEntity<Void> logicalDelete(@PathVariable Integer id) {
        Optional<Supplier> supplierOpt = supplierService.findById(id);
        if (supplierOpt.isPresent()) {
            Supplier supplier = supplierOpt.get();
            supplier.setStatus("I");
            supplierService.save(supplier);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PatchMapping("/restore/{id}")
    public ResponseEntity<Void> restore(@PathVariable Integer id) {
        Optional<Supplier> supplierOpt = supplierService.findById(id);
        if (supplierOpt.isPresent()) {
            Supplier supplier = supplierOpt.get();
            supplier.setStatus("A");
            supplierService.save(supplier);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/pdf")
    public ResponseEntity<byte[]> generateJasperPdfReport() {
        try {
            byte[] pdf = supplierService.generateJasperPdfReport();
            return ResponseEntity.ok()
                    // Renombrar el archivo PDF al descargar
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=reporte_proveedores.pdf")
                    .contentType(MediaType.APPLICATION_PDF)
                    .body(pdf);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

}
