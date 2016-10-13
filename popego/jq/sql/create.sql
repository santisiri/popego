--
-- PostgreSQL database dump
--

-- Started on 2008-04-23 12:04:13 ART

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 1471 (class 1259 OID 184615)
-- Dependencies: 3
-- Name: jobs; Type: TABLE; Schema: public; Owner: popego; Tablespace: 
--

CREATE TABLE jobs (
    id integer NOT NULL,
    queue_id integer NOT NULL,
    type text NOT NULL,
    data text,
    priority integer,
    creation_date timestamp without time zone NOT NULL,
    started_date timestamp without time zone,
    ended_date timestamp without time zone,
    error text
);


ALTER TABLE public.jobs OWNER TO popego;

--
-- TOC entry 1469 (class 1259 OID 184604)
-- Dependencies: 3
-- Name: queues; Type: TABLE; Schema: public; Owner: popego; Tablespace: 
--

CREATE TABLE queues (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.queues OWNER TO popego;

--
-- TOC entry 1470 (class 1259 OID 184613)
-- Dependencies: 3 1471
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: popego
--

CREATE SEQUENCE jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.jobs_id_seq OWNER TO popego;

--
-- TOC entry 1749 (class 0 OID 0)
-- Dependencies: 1470
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: popego
--

ALTER SEQUENCE jobs_id_seq OWNED BY jobs.id;


--
-- TOC entry 1468 (class 1259 OID 184602)
-- Dependencies: 3 1469
-- Name: queues_id_seq; Type: SEQUENCE; Schema: public; Owner: popego
--

CREATE SEQUENCE queues_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.queues_id_seq OWNER TO popego;

--
-- TOC entry 1750 (class 0 OID 0)
-- Dependencies: 1468
-- Name: queues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: popego
--

ALTER SEQUENCE queues_id_seq OWNED BY queues.id;


--
-- TOC entry 1739 (class 2604 OID 184618)
-- Dependencies: 1471 1470 1471
-- Name: id; Type: DEFAULT; Schema: public; Owner: popego
--

ALTER TABLE jobs ALTER COLUMN id SET DEFAULT nextval('jobs_id_seq'::regclass);


--
-- TOC entry 1738 (class 2604 OID 184607)
-- Dependencies: 1469 1468 1469
-- Name: id; Type: DEFAULT; Schema: public; Owner: popego
--

ALTER TABLE queues ALTER COLUMN id SET DEFAULT nextval('queues_id_seq'::regclass);


--
-- TOC entry 1743 (class 2606 OID 184623)
-- Dependencies: 1471 1471
-- Name: jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: popego; Tablespace: 
--

ALTER TABLE ONLY jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- TOC entry 1741 (class 2606 OID 184612)
-- Dependencies: 1469 1469
-- Name: queues_pkey; Type: CONSTRAINT; Schema: public; Owner: popego; Tablespace: 
--

ALTER TABLE ONLY queues
    ADD CONSTRAINT queues_pkey PRIMARY KEY (id);


--
-- TOC entry 1744 (class 2606 OID 184624)
-- Dependencies: 1740 1469 1471
-- Name: jobs_queue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: popego
--

ALTER TABLE ONLY jobs
    ADD CONSTRAINT jobs_queue_id_fkey FOREIGN KEY (queue_id) REFERENCES queues(id);


--
-- TOC entry 1748 (class 0 OID 0)
-- Dependencies: 3
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2008-04-23 12:04:13 ART

--
-- PostgreSQL database dump complete
--

