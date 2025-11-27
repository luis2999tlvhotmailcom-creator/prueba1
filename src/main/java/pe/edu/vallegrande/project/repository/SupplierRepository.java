package pe.edu.vallegrande.project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pe.edu.vallegrande.project.model.Supplier;

public interface SupplierRepository extends JpaRepository<Supplier, Integer> {
}

