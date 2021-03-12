-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 15-11-2020 a las 21:31:41
-- Versión del servidor: 10.5.6-MariaDB-1:10.5.6+maria~buster
-- Versión de PHP: 7.3.19-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto`
--
CREATE DATABASE IF NOT EXISTS `proyecto` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `proyecto`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aprobacion`
--

CREATE TABLE `aprobacion` (
  `id` int(11) NOT NULL,
  `tipo` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `aprobacion`
--

INSERT INTO `aprobacion` (`id`, `tipo`) VALUES
(1, 'Por Aprobar'),
(2, 'Aprobado'),
(3, 'Desaprobado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `centros_sociales`
--

CREATE TABLE `centros_sociales` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `hora_de_apertura` time NOT NULL,
  `hora_de_cierre` time NOT NULL,
  `municipio_id` int(11) NOT NULL,
  `web` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `tipo_centro_id` int(11) NOT NULL,
  `protocolo` varchar(255) DEFAULT NULL,
  `latitud` varchar(50) NOT NULL,
  `longitud` varchar(50) NOT NULL,
  `aprobacion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `centros_sociales`
--

INSERT INTO `centros_sociales` (`id`, `nombre`, `direccion`, `telefono`, `hora_de_apertura`, `hora_de_cierre`, `municipio_id`, `web`, `email`, `tipo_centro_id`, `protocolo`, `latitud`, `longitud`, `aprobacion_id`) VALUES
(30, 'Centro de ayuda Avellaneda', '9 de julio 1241', '11231231123', '09:00:00', '16:00:00', 1, '', '', 2, 'PROTOCOLO-1.pdf', '-34.66479719123736', '-58.364081974455445', 2),
(31, 'Centro Covid-19 La Plata', 'calle 4 1231', '2214124124', '09:00:00', '16:00:00', 19, '', '', 4, 'PROTOCOLO-2.pdf', '-34.91169351094561', '-57.946992121639774', 2),
(32, 'Centro La Matanza Ayuda', 'calle 23', '1231231', '09:00:00', '16:00:00', 1, 'lamatanzaayuda.com.ar', 'lmayuda@hotmail.com', 2, 'PROTOCOLO-3.pdf', '', '', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuraciones`
--

CREATE TABLE `configuraciones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `valor` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `configuraciones`
--

INSERT INTO `configuraciones` (`id`, `nombre`, `valor`) VALUES
(1, 'titulo', '          Ayudas Covid-19'),
(2, 'descripcion', ' Esta es una breve descripcion'),
(3, 'email', ' ayuda@ejemplo.com'),
(4, 'cantidad_elementos', '4'),
(5, 'habilitado', '1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `issues`
--

CREATE TABLE `issues` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `issues`
--

INSERT INTO `issues` (`id`, `email`, `description`, `category_id`, `status_id`) VALUES
(2, 'admin@admin.com', 'Este es un mensaje del admin', 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `nombre`) VALUES
(14, 'centro_aprobacion'),
(12, 'centro_destroy'),
(11, 'centro_index'),
(13, 'centro_new'),
(16, 'centro_show'),
(15, 'centro_update'),
(8, 'configuracion_destroy'),
(6, 'configuracion_index'),
(7, 'configuracion_new'),
(10, 'configuracion_show'),
(9, 'configuracion_update'),
(21, 'index_by_centro'),
(19, 'turno_destroy'),
(17, 'turno_index'),
(18, 'turno_new'),
(20, 'turno_update'),
(3, 'usuario_destroy'),
(1, 'usuario_index'),
(2, 'usuario_new'),
(5, 'usuario_show'),
(4, 'usuario_update');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre`) VALUES
(1, 'administrador'),
(2, 'operador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles_tienen_permisos`
--

CREATE TABLE `roles_tienen_permisos` (
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `roles_tienen_permisos`
--

INSERT INTO `roles_tienen_permisos` (`rol_id`, `permiso_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(2, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_centros`
--

CREATE TABLE `tipos_centros` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `tipos_centros`
--

INSERT INTO `tipos_centros` (`id`, `nombre`) VALUES
(1, 'Comida'),
(2, 'Ropa'),
(3, 'Abrigos'),
(4, 'Merendero'),
(5, 'Variado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `turnos`
--

CREATE TABLE `turnos` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(100) NOT NULL,
  `hora_inicio` time NOT NULL DEFAULT '00:00:00',
  `hora_fin` time NOT NULL DEFAULT '00:00:00',
  `fecha` date NOT NULL,
  `centro_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `turnos`
--

INSERT INTO `turnos` (`id`, `email`, `telefono`, `hora_inicio`, `hora_fin`, `fecha`, `centro_id`) VALUES
(1, 'emai@email.com', '', '09:30:00', '10:00:00', '2020-11-15', 30),
(2, 'email@donante.com', '123123124', '10:00:00', '10:30:00', '2020-11-15', 30),
(3, 'jp@jp.com', '91872938', '10:30:00', '11:00:00', '2020-11-15', 31),
(4, 'Solicitud@hotmail.com', '41982987', '10:00:00', '10:30:00', '2020-11-22', 31),
(6, 'jp@hotmail.com', '991872837', '10:00:00', '10:30:00', '2020-11-22', 32),
(7, 'jose@hotmail.com', '14981247', '09:30:00', '10:00:00', '2020-11-16', 32);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(128) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `password`, `active`, `first_name`, `last_name`) VALUES
(1, 'admin@admin.com', 'admin', 'admin', 1, 'adminfirst', 'adminlast'),
(3, 'federico@hotmail.com', 'fedeB', 'federico', 1, 'Federico', 'Bravin'),
(4, 'daniela@hotmail.com', 'DaniPR', 'daniela', 1, 'Daniela', 'Paredez Ruiz'),
(5, 'francisco@hotmail.com', 'Cisco', 'francisco', 1, 'Francisco', 'Torrealba Istillarte'),
(30, 'juampi@hotmail.com', 'JuampiNP', 'juampi', 1, 'Juan ', 'Nieva');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_tienen_roles`
--

CREATE TABLE `usuarios_tienen_roles` (
  `user_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuarios_tienen_roles`
--

INSERT INTO `usuarios_tienen_roles` (`user_id`, `rol_id`) VALUES
(1, 1),
(1, 2),
(3, 1),
(4, 1),
(5, 1),
(30, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `aprobacion`
--
ALTER TABLE `aprobacion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `centros_sociales`
--
ALTER TABLE `centros_sociales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tipo_centro_id` (`tipo_centro_id`),
  ADD KEY `aprobacion_id` (`aprobacion_id`);

--
-- Indices de la tabla `configuraciones`
--
ALTER TABLE `configuraciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `issues`
--
ALTER TABLE `issues`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `roles_tienen_permisos`
--
ALTER TABLE `roles_tienen_permisos`
  ADD PRIMARY KEY (`rol_id`,`permiso_id`),
  ADD KEY `rol_id` (`rol_id`),
  ADD KEY `permiso_id` (`permiso_id`);

--
-- Indices de la tabla `tipos_centros`
--
ALTER TABLE `tipos_centros`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `turnos`
--
ALTER TABLE `turnos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `usuarios_tienen_roles`
--
ALTER TABLE `usuarios_tienen_roles`
  ADD PRIMARY KEY (`user_id`,`rol_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `aprobacion`
--
ALTER TABLE `aprobacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `centros_sociales`
--
ALTER TABLE `centros_sociales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `issues`
--
ALTER TABLE `issues`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `turnos`
--
ALTER TABLE `turnos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `centros_sociales`
--
ALTER TABLE `centros_sociales`
  ADD CONSTRAINT `centros_sociales_ibfk_1` FOREIGN KEY (`tipo_centro_id`) REFERENCES `tipos_centros` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `roles`
--
ALTER TABLE `roles`
  ADD CONSTRAINT `roles_ibfk_1` FOREIGN KEY (`id`) REFERENCES `roles_tienen_permisos` (`rol_id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `roles_tienen_permisos`
--
ALTER TABLE `roles_tienen_permisos`
  ADD CONSTRAINT `roles_tienen_permisos_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `roles_tienen_permisos_ibfk_2` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuarios_tienen_roles`
--
ALTER TABLE `usuarios_tienen_roles`
  ADD CONSTRAINT `usuarios_tienen_roles_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
