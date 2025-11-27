package pe.edu.vallegrande.project.rest;

import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import pe.edu.vallegrande.project.model.Customer;
import pe.edu.vallegrande.project.service.CustomerService;

@CrossOrigin(origins = "*")
@Slf4j
@RestController
@RequestMapping("/v1/api/customer")
public class CustomerRest {

    private final CustomerService customerService;

    public CustomerRest(CustomerService customerService) {
        this.customerService = customerService;
    }

    // Obtener todos los clientes
    @GetMapping
    public List<Customer> findAll() {
        log.info("GET /v1/api/customer - Listar todos los clientes");
        return customerService.findAll();
    }

    // Obtener cliente por ID
    @GetMapping("/{id}")
    public ResponseEntity<Customer> findById(@PathVariable Long id) {
        log.info("GET /v1/api/customer/{} - Buscar cliente por ID", id);
        return customerService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // Crear nuevo cliente con validación de duplicados
    @PostMapping("/save")
    public ResponseEntity<?> save(@RequestBody @Valid Customer customer) {
        log.info("POST /v1/api/customer/save - Crear nuevo cliente: {}", customer);

        List<Customer> allCustomers = customerService.findAll();

        for (Customer existing : allCustomers) {
            if (existing.getEmail().equalsIgnoreCase(customer.getEmail())) {
                log.warn("⚠️ Correo ya en uso: {}", customer.getEmail());
                return ResponseEntity.status(409).body("Correo ya registrado por otro cliente.");
            }
            if (existing.getDocumentNumber().equals(customer.getDocumentNumber())) {
                log.warn("⚠️ Documento ya en uso: {}", customer.getDocumentNumber());
                return ResponseEntity.status(409).body("Número de documento ya registrado por otro cliente.");
            }
        }

        Customer savedCustomer = customerService.save(customer);
        return ResponseEntity.ok(savedCustomer);
    }

    // Actualizar cliente existente con validación de duplicados
    @PutMapping("/{id}")
    public ResponseEntity<?> updateCustomer(@PathVariable Long id, @RequestBody Customer updatedCustomer) {
        log.info("PUT /v1/api/customer/{} - Actualizar cliente", id);

        Optional<Customer> customerOpt = customerService.findById(id);
        if (customerOpt.isEmpty()) {
            log.warn("❌ Cliente con ID {} no encontrado", id);
            return ResponseEntity.notFound().build();
        }

        List<Customer> allCustomers = customerService.findAll();
        for (Customer existing : allCustomers) {
            if (!existing.getId().equals(id)) {
                if (existing.getEmail().equalsIgnoreCase(updatedCustomer.getEmail())) {
                    log.warn("⚠️ Correo ya en uso: {}", updatedCustomer.getEmail());
                    return ResponseEntity.status(409).body("Correo ya registrado por otro cliente.");
                }
                if (existing.getDocumentNumber().equals(updatedCustomer.getDocumentNumber())) {
                    log.warn("⚠️ Documento ya en uso: {}", updatedCustomer.getDocumentNumber());
                    return ResponseEntity.status(409).body("Número de documento ya registrado por otro cliente.");
                }
            }
        }

        Customer existingCustomer = customerOpt.get();
        existingCustomer.setName(updatedCustomer.getName());
        existingCustomer.setLastName(updatedCustomer.getLastName());
        existingCustomer.setPhone(updatedCustomer.getPhone());
        existingCustomer.setEmail(updatedCustomer.getEmail());
        existingCustomer.setAddress(updatedCustomer.getAddress());
        existingCustomer.setIdentificationDocument(updatedCustomer.getIdentificationDocument());
        existingCustomer.setDocumentNumber(updatedCustomer.getDocumentNumber());
        existingCustomer.setStatus(updatedCustomer.getStatus());

        Customer savedCustomer = customerService.update(existingCustomer);
        log.info("✅ Cliente actualizado con éxito: {}", savedCustomer);
        return ResponseEntity.ok(savedCustomer);
    }

    // Eliminar cliente permanentemente
    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        log.info("DELETE /v1/api/customer/{} - Eliminar cliente", id);
        customerService.delete(id);
    }

    // Eliminación lógica (cambia el estado a "I")
    @DeleteMapping("/logical/{id}")
    public ResponseEntity<Void> logicalDelete(@PathVariable Long id) {
        log.info("DELETE /v1/api/customer/logical/{} - Eliminación lógica", id);
        Optional<Customer> customerOpt = customerService.findById(id);
        if (customerOpt.isPresent()) {
            Customer customer = customerOpt.get();
            customer.setStatus("I");
            customerService.save(customer);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // Restaurar cliente eliminado lógicamente
    @PutMapping("/restore/{id}")
    public ResponseEntity<Void> restore(@PathVariable Long id) {
        log.info("PUT /v1/api/customer/restore/{} - Restaurar cliente", id);
        Optional<Customer> customerOpt = customerService.findById(id);
        if (customerOpt.isPresent()) {
            Customer customer = customerOpt.get();
            customer.setStatus("A");
            customerService.save(customer);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // Descargar reporte PDF usando JasperReports
    @GetMapping("/pdf")
    public ResponseEntity<byte[]> generateJasperPdfReport() {
        log.info("GET /v1/api/customer/pdf - Generar reporte PDF");
        try {
            byte[] pdf = customerService.generateJasperPdfReport();
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=reporte_clientes.pdf")
                    .contentType(MediaType.APPLICATION_PDF)
                    .body(pdf);
        } catch (Exception e) {
            log.error("Error al generar el PDF", e);
            return ResponseEntity.internalServerError().build();
        }
    }
}
