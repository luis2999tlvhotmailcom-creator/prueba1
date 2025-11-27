package pe.edu.vallegrande.project.repository;

import pe.edu.vallegrande.project.model.Seller;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SellerRepository extends JpaRepository<Seller, Long> {
}
