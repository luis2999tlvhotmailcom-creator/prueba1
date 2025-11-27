package pe.edu.vallegrande.project.service;

import java.util.List;
import java.util.Optional;

import pe.edu.vallegrande.project.model.Seller;

public interface SellerService {

    List<Seller> findAll();
    Optional<Seller> findById(Long id);
    Seller save(Seller seller);
    Seller update(Seller seller);
    void delete(Long id);
}
