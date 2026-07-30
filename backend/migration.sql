BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 3312fde260b3

CREATE TABLE role (
    id UUID NOT NULL, 
    name VARCHAR(50) NOT NULL, 
    description VARCHAR(255), 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_role_name ON role (name);

CREATE TABLE "user" (
    id UUID NOT NULL, 
    full_name VARCHAR(150) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    mobile VARCHAR(20), 
    password_hash VARCHAR(255) NOT NULL, 
    role_id UUID NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    is_verified BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(role_id) REFERENCES role (id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX ix_user_email ON "user" (email);

CREATE INDEX ix_user_role_id ON "user" (role_id);

INSERT INTO alembic_version (version_num) VALUES ('3312fde260b3') RETURNING alembic_version.version_num;

-- Running upgrade 3312fde260b3 -> b637615eb45d

CREATE TABLE refresh_token (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    jti VARCHAR(36) NOT NULL, 
    token_hash VARCHAR(255) NOT NULL, 
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL, 
    revoked_at TIMESTAMP WITH TIME ZONE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_refresh_token_jti ON refresh_token (jti);

CREATE INDEX ix_refresh_token_user_id ON refresh_token (user_id);

CREATE INDEX ix_refresh_token_expires_at ON refresh_token (expires_at);

UPDATE alembic_version SET version_num='b637615eb45d' WHERE alembic_version.version_num = '3312fde260b3';

-- Running upgrade b637615eb45d -> 43f4014f93cb

CREATE TABLE temple (
    id UUID NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    slug VARCHAR(255) NOT NULL, 
    description TEXT, 
    email VARCHAR(255), 
    phone VARCHAR(20), 
    website VARCHAR(255), 
    address TEXT NOT NULL, 
    city VARCHAR(100) NOT NULL, 
    state VARCHAR(100) NOT NULL, 
    country VARCHAR(100) NOT NULL, 
    postal_code VARCHAR(20), 
    latitude VARCHAR(50), 
    longitude VARCHAR(50), 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_temple_name ON temple (name);

CREATE UNIQUE INDEX ix_temple_slug ON temple (slug);

UPDATE alembic_version SET version_num='43f4014f93cb' WHERE alembic_version.version_num = 'b637615eb45d';

-- Running upgrade 43f4014f93cb -> 1923bb3512e1

CREATE TABLE category (
    id UUID NOT NULL, 
    temple_id UUID NOT NULL, 
    name VARCHAR(150) NOT NULL, 
    slug VARCHAR(150) NOT NULL, 
    description TEXT, 
    display_order INTEGER NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(temple_id) REFERENCES temple (id) ON DELETE CASCADE
);

CREATE INDEX ix_category_name ON category (name);

CREATE UNIQUE INDEX ix_category_slug ON category (slug);

CREATE INDEX ix_category_temple_id ON category (temple_id);

DROP INDEX ix_refresh_token_expires_at;

UPDATE alembic_version SET version_num='1923bb3512e1' WHERE alembic_version.version_num = '43f4014f93cb';

-- Running upgrade 1923bb3512e1 -> efa51db78459

CREATE TABLE priest (
    id UUID NOT NULL, 
    temple_id UUID NOT NULL, 
    full_name VARCHAR(150) NOT NULL, 
    email VARCHAR(255), 
    phone VARCHAR(20) NOT NULL, 
    experience_years INTEGER NOT NULL, 
    specialization VARCHAR(255), 
    bio TEXT, 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(temple_id) REFERENCES temple (id) ON DELETE CASCADE, 
    UNIQUE (email), 
    UNIQUE (phone)
);

CREATE INDEX ix_priest_full_name ON priest (full_name);

CREATE INDEX ix_priest_temple_id ON priest (temple_id);

UPDATE alembic_version SET version_num='efa51db78459' WHERE alembic_version.version_num = '1923bb3512e1';

-- Running upgrade efa51db78459 -> 2df888a4c334

CREATE TABLE pooja (
    id UUID NOT NULL, 
    temple_id UUID NOT NULL, 
    category_id UUID NOT NULL, 
    priest_id UUID, 
    name VARCHAR(255) NOT NULL, 
    slug VARCHAR(255) NOT NULL, 
    description TEXT, 
    duration_minutes INTEGER NOT NULL, 
    price NUMERIC(10, 2) NOT NULL, 
    max_participants INTEGER NOT NULL, 
    online_booking BOOLEAN NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(category_id) REFERENCES category (id) ON DELETE RESTRICT, 
    FOREIGN KEY(priest_id) REFERENCES priest (id) ON DELETE SET NULL, 
    FOREIGN KEY(temple_id) REFERENCES temple (id) ON DELETE CASCADE
);

CREATE INDEX ix_pooja_category_id ON pooja (category_id);

CREATE INDEX ix_pooja_name ON pooja (name);

CREATE INDEX ix_pooja_priest_id ON pooja (priest_id);

CREATE UNIQUE INDEX ix_pooja_slug ON pooja (slug);

CREATE INDEX ix_pooja_temple_id ON pooja (temple_id);

UPDATE alembic_version SET version_num='2df888a4c334' WHERE alembic_version.version_num = 'efa51db78459';

-- Running upgrade 2df888a4c334 -> 0469b2e1b595

CREATE TABLE booking (
    id UUID NOT NULL, 
    booking_number VARCHAR(30) NOT NULL, 
    user_id UUID NOT NULL, 
    temple_id UUID NOT NULL, 
    pooja_id UUID NOT NULL, 
    booking_date DATE NOT NULL, 
    booking_time TIME WITHOUT TIME ZONE NOT NULL, 
    participants INTEGER NOT NULL, 
    devotee_name VARCHAR(150) NOT NULL, 
    devotee_mobile VARCHAR(20) NOT NULL, 
    devotee_email VARCHAR(255), 
    special_notes TEXT, 
    booking_status VARCHAR(30) NOT NULL, 
    payment_status VARCHAR(30) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(pooja_id) REFERENCES pooja (id) ON DELETE RESTRICT, 
    FOREIGN KEY(temple_id) REFERENCES temple (id) ON DELETE CASCADE, 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_booking_booking_number ON booking (booking_number);

CREATE INDEX ix_booking_user_id ON booking (user_id);

UPDATE alembic_version SET version_num='0469b2e1b595' WHERE alembic_version.version_num = '2df888a4c334';

-- Running upgrade 0469b2e1b595 -> 6661918420a0

CREATE TABLE payment (
    id UUID NOT NULL, 
    booking_id UUID NOT NULL, 
    transaction_id VARCHAR(150), 
    amount NUMERIC(10, 2) NOT NULL, 
    payment_method VARCHAR(50), 
    payment_status VARCHAR(30) NOT NULL, 
    gateway VARCHAR(50), 
    gateway_payment_id VARCHAR(150), 
    failure_reason TEXT, 
    paid_at TIMESTAMP WITH TIME ZONE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(booking_id) REFERENCES booking (id) ON DELETE CASCADE
);

CREATE INDEX ix_payment_booking_id ON payment (booking_id);

CREATE INDEX ix_payment_payment_status ON payment (payment_status);

CREATE UNIQUE INDEX ix_payment_transaction_id ON payment (transaction_id);

UPDATE alembic_version SET version_num='6661918420a0' WHERE alembic_version.version_num = '0469b2e1b595';

-- Running upgrade 6661918420a0 -> 26ce990541b1

CREATE TABLE invoice (
    id UUID NOT NULL, 
    invoice_number VARCHAR(50) NOT NULL, 
    booking_id UUID NOT NULL, 
    payment_id UUID, 
    subtotal NUMERIC(10, 2) NOT NULL, 
    tax_amount NUMERIC(10, 2) NOT NULL, 
    discount_amount NUMERIC(10, 2) NOT NULL, 
    total_amount NUMERIC(10, 2) NOT NULL, 
    invoice_status VARCHAR(30) NOT NULL, 
    notes TEXT, 
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(booking_id) REFERENCES booking (id) ON DELETE CASCADE, 
    FOREIGN KEY(payment_id) REFERENCES payment (id) ON DELETE SET NULL
);

CREATE INDEX ix_invoice_booking_id ON invoice (booking_id);

CREATE UNIQUE INDEX ix_invoice_invoice_number ON invoice (invoice_number);

CREATE INDEX ix_invoice_invoice_status ON invoice (invoice_status);

CREATE INDEX ix_invoice_payment_id ON invoice (payment_id);

UPDATE alembic_version SET version_num='26ce990541b1' WHERE alembic_version.version_num = '6661918420a0';

-- Running upgrade 26ce990541b1 -> 3a5de343584c

CREATE TABLE gallery (
    id UUID NOT NULL, 
    temple_id UUID, 
    pooja_id UUID, 
    title VARCHAR(150), 
    description TEXT, 
    media_url VARCHAR(500) NOT NULL, 
    media_type VARCHAR(30) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(pooja_id) REFERENCES pooja (id) ON DELETE CASCADE, 
    FOREIGN KEY(temple_id) REFERENCES temple (id) ON DELETE CASCADE
);

CREATE INDEX ix_gallery_pooja_id ON gallery (pooja_id);

CREATE INDEX ix_gallery_temple_id ON gallery (temple_id);

UPDATE alembic_version SET version_num='3a5de343584c' WHERE alembic_version.version_num = '26ce990541b1';

-- Running upgrade 3a5de343584c -> 71ca6a0b6378

CREATE TABLE notification (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    title VARCHAR(200) NOT NULL, 
    message TEXT NOT NULL, 
    notification_type VARCHAR(50) NOT NULL, 
    reference_id VARCHAR(100), 
    is_read BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE INDEX ix_notification_is_read ON notification (is_read);

CREATE INDEX ix_notification_notification_type ON notification (notification_type);

CREATE INDEX ix_notification_user_id ON notification (user_id);

UPDATE alembic_version SET version_num='71ca6a0b6378' WHERE alembic_version.version_num = '3a5de343584c';

-- Running upgrade 71ca6a0b6378 -> 35bbbf846ae8

CREATE TABLE review (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    booking_id UUID NOT NULL, 
    pooja_id UUID NOT NULL, 
    rating INTEGER NOT NULL, 
    review_text TEXT, 
    review_status VARCHAR(30) NOT NULL, 
    admin_response TEXT, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    CONSTRAINT ck_review_rating_range CHECK (rating >= 1 AND rating <= 5), 
    FOREIGN KEY(booking_id) REFERENCES booking (id) ON DELETE CASCADE, 
    FOREIGN KEY(pooja_id) REFERENCES pooja (id) ON DELETE CASCADE, 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE, 
    CONSTRAINT uq_review_booking_id UNIQUE (booking_id)
);

CREATE INDEX ix_review_booking_id ON review (booking_id);

CREATE INDEX ix_review_pooja_id ON review (pooja_id);

CREATE INDEX ix_review_rating ON review (rating);

CREATE INDEX ix_review_review_status ON review (review_status);

CREATE INDEX ix_review_user_id ON review (user_id);

UPDATE alembic_version SET version_num='35bbbf846ae8' WHERE alembic_version.version_num = '71ca6a0b6378';

-- Running upgrade 35bbbf846ae8 -> a60f57740a9b

CREATE TABLE contact (
    id UUID NOT NULL, 
    name VARCHAR(150) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    phone VARCHAR(30), 
    subject VARCHAR(255), 
    message TEXT NOT NULL, 
    enquiry_status VARCHAR(30) DEFAULT 'NEW' NOT NULL, 
    admin_notes TEXT, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_contact_email ON contact (email);

CREATE INDEX ix_contact_enquiry_status ON contact (enquiry_status);

UPDATE alembic_version SET version_num='a60f57740a9b' WHERE alembic_version.version_num = '35bbbf846ae8';

-- Running upgrade a60f57740a9b -> 3195993d9cde

CREATE TABLE catering (
    id UUID NOT NULL, 
    temple_id UUID, 
    pooja_id UUID, 
    name VARCHAR(150) NOT NULL, 
    service_type VARCHAR(30) DEFAULT 'CATERING' NOT NULL, 
    description TEXT, 
    menu_details TEXT, 
    price_per_person NUMERIC(10, 2) NOT NULL, 
    minimum_people INTEGER DEFAULT '1' NOT NULL, 
    maximum_people INTEGER, 
    is_vegetarian BOOLEAN DEFAULT 'true' NOT NULL, 
    is_available BOOLEAN DEFAULT 'true' NOT NULL, 
    image_url VARCHAR(500), 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(pooja_id) REFERENCES pooja (id) ON DELETE SET NULL, 
    FOREIGN KEY(temple_id) REFERENCES temple (id) ON DELETE CASCADE
);

CREATE INDEX ix_catering_is_available ON catering (is_available);

CREATE INDEX ix_catering_pooja_id ON catering (pooja_id);

CREATE INDEX ix_catering_service_type ON catering (service_type);

CREATE INDEX ix_catering_temple_id ON catering (temple_id);

UPDATE alembic_version SET version_num='3195993d9cde' WHERE alembic_version.version_num = 'a60f57740a9b';

-- Running upgrade 3195993d9cde -> c423ae36ab09

CREATE TABLE kundli (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    priest_id UUID, 
    full_name VARCHAR(150) NOT NULL, 
    date_of_birth DATE NOT NULL, 
    time_of_birth TIME WITHOUT TIME ZONE NOT NULL, 
    place_of_birth VARCHAR(255) NOT NULL, 
    gender VARCHAR(30), 
    service_type VARCHAR(50) DEFAULT 'KUNDLI' NOT NULL, 
    request_status VARCHAR(30) DEFAULT 'PENDING' NOT NULL, 
    user_question TEXT, 
    report_url VARCHAR(500), 
    admin_notes TEXT, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(priest_id) REFERENCES priest (id) ON DELETE SET NULL, 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE INDEX ix_kundli_priest_id ON kundli (priest_id);

CREATE INDEX ix_kundli_request_status ON kundli (request_status);

CREATE INDEX ix_kundli_service_type ON kundli (service_type);

CREATE INDEX ix_kundli_user_id ON kundli (user_id);

UPDATE alembic_version SET version_num='c423ae36ab09' WHERE alembic_version.version_num = '3195993d9cde';

-- Running upgrade c423ae36ab09 -> cf4dd928f80e

CREATE TABLE consultation (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    priest_id UUID, 
    kundli_id UUID, 
    consultation_type VARCHAR(30) DEFAULT 'VIDEO' NOT NULL, 
    consultation_status VARCHAR(30) DEFAULT 'PENDING' NOT NULL, 
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL, 
    duration_minutes INTEGER DEFAULT '30' NOT NULL, 
    consultation_fee NUMERIC(10, 2) DEFAULT '0' NOT NULL, 
    topic VARCHAR(255), 
    user_question TEXT, 
    meeting_url VARCHAR(1000), 
    meeting_id VARCHAR(255), 
    admin_notes TEXT, 
    priest_notes TEXT, 
    started_at TIMESTAMP WITH TIME ZONE, 
    ended_at TIMESTAMP WITH TIME ZONE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(kundli_id) REFERENCES kundli (id) ON DELETE SET NULL, 
    FOREIGN KEY(priest_id) REFERENCES priest (id) ON DELETE SET NULL, 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE INDEX ix_consultation_consultation_status ON consultation (consultation_status);

CREATE INDEX ix_consultation_consultation_type ON consultation (consultation_type);

CREATE INDEX ix_consultation_kundli_id ON consultation (kundli_id);

CREATE INDEX ix_consultation_priest_id ON consultation (priest_id);

CREATE INDEX ix_consultation_scheduled_at ON consultation (scheduled_at);

CREATE INDEX ix_consultation_user_id ON consultation (user_id);

UPDATE alembic_version SET version_num='cf4dd928f80e' WHERE alembic_version.version_num = 'c423ae36ab09';

-- Running upgrade cf4dd928f80e -> 19fe601306ad

CREATE TABLE chat_conversation (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    title VARCHAR(255), 
    conversation_status VARCHAR(30) DEFAULT 'ACTIVE' NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE INDEX ix_chat_conversation_conversation_status ON chat_conversation (conversation_status);

CREATE INDEX ix_chat_conversation_user_id ON chat_conversation (user_id);

CREATE TABLE chat_message (
    id UUID NOT NULL, 
    conversation_id UUID NOT NULL, 
    role VARCHAR(30) NOT NULL, 
    content TEXT NOT NULL, 
    model_name VARCHAR(100), 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(conversation_id) REFERENCES chat_conversation (id) ON DELETE CASCADE
);

CREATE INDEX ix_chat_message_conversation_id ON chat_message (conversation_id);

CREATE INDEX ix_chat_message_role ON chat_message (role);

UPDATE alembic_version SET version_num='19fe601306ad' WHERE alembic_version.version_num = 'cf4dd928f80e';

-- Running upgrade 19fe601306ad -> e9e7cc52aa2f

CREATE TYPE booking_status_enum AS ENUM ('REQUESTED', 'REVIEWING', 'CUSTOMER_CONTACTED', 'QUOTATION_PREPARING', 'QUOTATION_SENT', 'WAITING_FOR_CUSTOMER', 'QUOTATION_ACCEPTED', 'ADVANCE_PAYMENT_PENDING', 'ADVANCE_PAID', 'PAYMENT_VERIFIED', 'PRIEST_ASSIGNED', 'CATERING_ASSIGNED', 'MATERIALS_READY', 'CALENDAR_SHARED', 'SERVICE_IN_PROGRESS', 'SERVICE_COMPLETED', 'FINAL_PAYMENT_PENDING', 'COMPLETED', 'CANCELLED');

CREATE TYPE quotation_status_enum AS ENUM ('DRAFT', 'SENT', 'VIEWED', 'ACCEPTED', 'REJECTED', 'EXPIRED', 'CANCELLED');

UPDATE booking
        SET booking_status='REQUESTED'
        WHERE booking_status='PENDING';

UPDATE booking
        SET booking_status='COMPLETED'
        WHERE booking_status='CONFIRMED';

ALTER TABLE booking ALTER COLUMN booking_status TYPE booking_status_enum USING booking_status::booking_status_enum;

CREATE TYPE quotation_status_enum AS ENUM ('DRAFT', 'SENT', 'VIEWED', 'ACCEPTED', 'REJECTED', 'EXPIRED', 'CANCELLED');

CREATE TABLE booking_quotation (
    id UUID NOT NULL, 
    booking_id UUID NOT NULL, 
    quotation_number VARCHAR(30) NOT NULL, 
    priest_cost NUMERIC(10, 2) NOT NULL, 
    material_cost NUMERIC(10, 2) NOT NULL, 
    catering_cost NUMERIC(10, 2) NOT NULL, 
    transport_cost NUMERIC(10, 2) NOT NULL, 
    miscellaneous_cost NUMERIC(10, 2) NOT NULL, 
    discount NUMERIC(10, 2) NOT NULL, 
    tax NUMERIC(10, 2) NOT NULL, 
    total_amount NUMERIC(10, 2) NOT NULL, 
    advance_amount NUMERIC(10, 2) NOT NULL, 
    remaining_amount NUMERIC(10, 2) NOT NULL, 
    notes TEXT, 
    quotation_status quotation_status_enum NOT NULL, 
    accepted_at TIMESTAMP WITH TIME ZONE, 
    valid_until TIMESTAMP WITH TIME ZONE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(booking_id) REFERENCES booking (id) ON DELETE CASCADE, 
    UNIQUE (quotation_number)
);

CREATE UNIQUE INDEX ix_booking_quotation_booking_id ON booking_quotation (booking_id);

CREATE TYPE booking_status_enum AS ENUM ('REQUESTED', 'REVIEWING', 'CUSTOMER_CONTACTED', 'QUOTATION_PREPARING', 'QUOTATION_SENT', 'WAITING_FOR_CUSTOMER', 'QUOTATION_ACCEPTED', 'ADVANCE_PAYMENT_PENDING', 'ADVANCE_PAID', 'PAYMENT_VERIFIED', 'PRIEST_ASSIGNED', 'CATERING_ASSIGNED', 'MATERIALS_READY', 'CALENDAR_SHARED', 'SERVICE_IN_PROGRESS', 'SERVICE_COMPLETED', 'FINAL_PAYMENT_PENDING', 'COMPLETED', 'CANCELLED');

CREATE TABLE booking_status_history (
    id UUID NOT NULL, 
    booking_id UUID NOT NULL, 
    status booking_status_enum NOT NULL, 
    remarks TEXT, 
    updated_by VARCHAR(100) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(booking_id) REFERENCES booking (id) ON DELETE CASCADE
);

CREATE INDEX ix_booking_status_history_booking_id ON booking_status_history (booking_id);

CREATE TABLE priest_assignment (
    id UUID NOT NULL, 
    booking_id UUID NOT NULL, 
    priest_id UUID NOT NULL, 
    assigned_by UUID NOT NULL, 
    notes TEXT, 
    is_confirmed BOOLEAN NOT NULL, 
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(assigned_by) REFERENCES "user" (id), 
    FOREIGN KEY(booking_id) REFERENCES booking (id) ON DELETE CASCADE, 
    FOREIGN KEY(priest_id) REFERENCES priest (id) ON DELETE RESTRICT, 
    UNIQUE (booking_id)
);

UPDATE alembic_version SET version_num='e9e7cc52aa2f' WHERE alembic_version.version_num = '19fe601306ad';

COMMIT;

