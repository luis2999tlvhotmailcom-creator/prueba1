package pe.edu.vallegrande.project.service.impl;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import lombok.extern.slf4j.Slf4j;
import pe.edu.vallegrande.project.model.Seller;
import pe.edu.vallegrande.project.repository.SellerRepository;
import pe.edu.vallegrande.project.service.SellerService;

@Slf4j
@Service
public class SellerServiceImpl implements SellerService {

    private final SellerRepository sellerRepository;

    public SellerServiceImpl(SellerRepository sellerRepository) {
        this.sellerRepository = sellerRepository;
    }

    @Override
    public List<Seller> findAll() {
        log.info("Listando datos de vendedores");
        return sellerRepository.findAll();
    }

    @Override
    public Optional<Seller> findById(Long id) {
        log.info("Buscando vendedor por ID: " + id);
        return sellerRepository.findById(id);
    }

    @Override
    public Seller save(Seller seller) {
        log.info("Registrando nuevo vendedor: " + seller.toString());
        return sellerRepository.save(seller);
    }

    @Override
    public Seller update(Seller seller) {
        log.info("Actualizando datos del vendedor: " + seller.toString());
        return sellerRepository.save(seller);
    }

    @Override
    public void delete(Long id) {
        log.info("Eliminando vendedor con ID: " + id);
        sellerRepository.deleteById(id);
    }
}
