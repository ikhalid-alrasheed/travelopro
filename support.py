from datetime import datetime as dt 

def to_flights(f):
    output={}
    output["FareSourceCode"] = f["AirItineraryFareInfo"]["FareSourceCode"]
    output["price"] = "USD " + f["AirItineraryFareInfo"]["ItinTotalFares"]["TotalFare"]["Amount"] 
    output["airline"] = f["ValidatingAirlineCode"]
    output["stops"] = f["OriginDestinationOptions"][0]["TotalStops"]
    output["IsPassportMandatory"] = int(f["IsPassportMandatory"] == "true")
    output["sets"] = f["OriginDestinationOptions"][0]["OriginDestinationOption"][0]["SeatsRemaining"]["Number"]
    output["from_airport"] = f["OriginDestinationOptions"][0]["OriginDestinationOption"][0]["FlightSegment"]["DepartureAirportLocationCode"]
    output["to_airport"] = f["OriginDestinationOptions"][0]["OriginDestinationOption"][-1]["FlightSegment"]["ArrivalAirportLocationCode"]
    output["arrive_at"] = f["OriginDestinationOptions"][0]["OriginDestinationOption"][-1]["FlightSegment"]["ArrivalDateTime"]
    output["depart_at"] = f["OriginDestinationOptions"][0]["OriginDestinationOption"][0]["FlightSegment"]["DepartureDateTime"]
    output["flight_info"] = f'{f["OriginDestinationOptions"][0]["OriginDestinationOption"][0]["FlightSegment"]["MarketingAirlineCode"]}-{f["OriginDestinationOptions"][0]["OriginDestinationOption"][0]["FlightSegment"]["FlightNumber"]}'
    output["flight_type"] = "LCC" if "ResBookDesigText" in f["OriginDestinationOptions"][0]["OriginDestinationOption"][0].keys() else "Other" 
    dur = (dt.fromisoformat(output["arrive_at"]) - dt.fromisoformat(output["depart_at"])).total_seconds()
    output["trip_duration"] = f'{int(dur//3600)}h{int((dur%3600)/60)}m'
    return output

def validated_flight(flight):
    output = {}
    f = flight["AirRevalidateResponse"]["AirRevalidateResult"]
    output["IsValid"] = f["IsValid"]
    s = [x["Service"] for x in f["ExtraServices"]["Services"]]
    f = f["FareItineraries"]["FareItinerary"]["AirItineraryFareInfo"]
    price_break = f["FareBreakdown"]
    
    output["breakDown"] = []
    for price in price_break:
        t = price["PassengerTypeQuantity"]
        for i in range(int(t["Quantity"])):
            a = {}
            a["T"] = f'{"Adult " if t["Code"]=="ADT" else "Childe " if t["Code"]=="CHD" else "Invent "}{str(i+1)}'
            tax = f'{sum([float(price["PassengerFare"]["ServiceTax"]["Amount"])] + [float(x["Amount"]) for x in price["PassengerFare"]["Taxes"]]):.2f}'
            a["prices"] = { "base": "USD " + price["PassengerFare"]["EquivFare"]["Amount"],
                            "tax": "USD " + tax,
                            "total": "USD " + price["PassengerFare"]["TotalFare"]["Amount"]}
            output["breakDown"].append(a)
    output["total"] = {"base":"USD " + f["ItinTotalFares"]["EquivFare"]["Amount"],
                        "tax":"USD " + f["ItinTotalFares"]["TotalTax"]["Amount"],
                       "service" : "USD " + f["ItinTotalFares"]["ServiceTax"]["Amount"],
                       "total" :  "USD " + f["ItinTotalFares"]["TotalFare"]["Amount"]}

    output["FareSourceCode"] = f["FareSourceCode"]
    return output
    