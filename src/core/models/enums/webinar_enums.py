class WebinarApplicationType:
    JSFP = "JSFP"
    COMPANY = "COMPANY"
    PRIVATE_PERSON = "PRIVATE_PERSON"


class WebinarApplicationStep:
    APPLICATION_TYPE = "APPLICATION_TYPE"
    PERSON_DETAILS = "PERSON_DETAILS"
    BUYER = "BUYER"
    RECIPIENT = "RECIPIENT"
    INVOICE = "INVOICE"
    SUBMITTER = "SUBMITTER"
    PARTICIPANTS = "PARTICIPANTS"
    ADDITIONAL_INFO = "ADD_INFO"
    SUMMARY = "SUMMARY"


class WebinarStatus:
    INIT = "INIT"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    DONE = "DONE"


class WebinarDuration:
    H1_M00 = "60"
    H1_M30 = "90"
    H2_M00 = "120"
    H2_M30 = "150"
    H3_M00 = "180"
    H3_M30 = "210"
    H4_M00 = "240"
    H4_M30 = "270"
    H5_M00 = "300"
    H5_M30 = "330"
    H6_M00 = "360"
    H6_M30 = "390"
    H7_M00 = "420"
    H7_M30 = "450"
    H8_M00 = "480"
    H8_M30 = "510"
    H9_M00 = "540"


WEBINAR_CLICKMEETING_DURATION = {
    WebinarDuration.H1_M00: "1:00",
    WebinarDuration.H1_M30: "1:30",
    WebinarDuration.H2_M00: "2:00",
    WebinarDuration.H2_M30: "2:30",
    WebinarDuration.H3_M00: "3:00",
    WebinarDuration.H3_M30: "3:30",
    WebinarDuration.H4_M00: "4:00",
    WebinarDuration.H4_M30: "4:30",
    WebinarDuration.H5_M00: "5:00",
    WebinarDuration.H5_M30: "5:30",
    WebinarDuration.H6_M00: "6:00",
    WebinarDuration.H6_M30: "6:30",
    WebinarDuration.H7_M00: "7:00",
    WebinarDuration.H7_M30: "7:30",
    WebinarDuration.H8_M00: "8:00",
    WebinarDuration.H8_M30: "8:30",
    WebinarDuration.H9_M00: "9:00",
}
