package pe.edu.vallegrande.project.config;

import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;

//Configuración para evitar el error ParserConfigurationException en el reporte de Jasper
@Configuration
public class JasperXmlFixConfig {

    @PostConstruct
    public void fixXmlParser() {
        System.setProperty(
            "javax.xml.parsers.DocumentBuilderFactory",
            "com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl"
        );
    }

}
