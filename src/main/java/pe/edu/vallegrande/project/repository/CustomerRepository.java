package pe.edu.vallegrande.project.repository;

import pe.edu.vallegrande.project.model.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRepository extends JpaRepository<Customer, Long> {
    
}