package pe.edu.vallegrande.project.config;

import java.util.List;

import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.xml.MappingJackson2XmlHttpMessageConverter;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void extendMessageConverters(List<HttpMessageConverter<?>> converters) {
        // Elimina el convertidor XML para evitar que las respuestas se serialicen en XML
        converters.removeIf(c -> c instanceof MappingJackson2XmlHttpMessageConverter);
    }
}