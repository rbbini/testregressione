//import { makeDistroChart } from './distrochart.js';
var http = new XMLHttpRequest();
let javascript_data = {};
/* fare la get dal sessionstorage */
let dataType = 'physical';
const jsonControfact = {
    'counterfactual':
            {'physical': [
                ['anni_ricovero', 8.36, 7.29, 6.220000000000001, 5.144, 4.07, 3.0, 1.93, 0.8559999999999999, -0.2200000000000002, -1.29, -2.3600000000000003], ['SF12_PhysicalScore_PreOp', 6.9399999999999995, 6.15, 5.359999999999999, 4.58, 3.7880000000000003, 3.0, 2.2119999999999997, 1.42, 0.6400000000000001, -0.1499999999999999, -0.94]
                ],
                'mental': [
                    ['SF12_PhysicalScore_PreOp', 6.9399999999999995, 6.15, 5.359999999999999, 4.58, 3.7880000000000003, 3.0, 2.2119999999999997, 1.42, 0.6400000000000001, -0.1499999999999999, -0.94], ['SF12_MentalScore_PreOp', 9.11, 7.89, 6.66, 5.4399999999999995, 4.22, 3.0, 1.78, 0.56, -0.6600000000000001, -1.8899999999999997, -3.1100000000000003]
                ]
            },
        'predictions': [
            {'SF12_PhysicalScore_6months': [38.3406572248497], 'SF12_MentalScore_6months': [38.80162549314018], 'age': [3]},
            [{'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.27150789362343]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.040320754089805]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [38.80913361455619]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.580872894510335]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.34910047107916]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.118498615443094]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [37.88789675980702]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.65612433637585]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.42786361633]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.19667647679638]}, {'anni_ricovero': 8.36, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [36.96548933726275]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.315856720501245]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.08466958096762]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [38.853482441434]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.625221721388144]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.39344929795698]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.16284744232091]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [37.932245586684836]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.70047316325366]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.47221244320781]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.24102530367419]}, {'anni_ricovero': 7.29, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.00983816414057]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.36020554737905]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.129018407845436]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [38.89783126831181]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.66957054826596]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.437798124834785]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.20719626919872]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [37.97659441356265]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.74482199013147]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.51656127008562]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.285374130552]}, {'anni_ricovero': 6.220000000000001, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.05418699101838]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.404803059267394]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.17361591973378]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [38.94242878020015]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.7141680601543]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.482395636723126]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.25179378108706]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.02119192545099]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.78941950201981]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.56115878197396]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.32997164244034]}, {'anni_ricovero': 5.144, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.098784502906724]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.44931767615222]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.2181305366186]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [38.986943397084985]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.75868267703913]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.52691025360795]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.296308397971885]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.06570654233582]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.833934118904644]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.60567339885879]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.37448625932517]}, {'anni_ricovero': 4.07, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.14329911979155]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.493666503030035]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.26247936349641]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [39.031292223962794]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.80303150391694]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.57125908048577]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.3406572248497]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.110055369213626]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.87828294578246]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.650022225736606]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.41883508620298]}, {'anni_ricovero': 3.0, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.18764794666936]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.53801532990785]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.306828190374226]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [39.0756410508406]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.84738033079475]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.61560790736358]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.385006051727515]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.15440419609144]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.92263177266027]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.694371052614414]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.4631839130808]}, {'anni_ricovero': 1.93, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.23199677354717]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.582529946792675]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.35134280725906]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [39.12015566772544]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.89189494767959]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.66012252424841]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.42952066861234]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.198918812976274]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [37.9671463895451]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.73888566949925]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.50769852996562]}, {'anni_ricovero': 0.8559999999999999, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.276511390432006]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.62712745868102]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.3959403191474]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [39.16475317961378]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.93649245956793]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.70472003613675]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.47411818050068]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.243516324864615]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [38.01174390143344]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.78348318138759]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.552296041853964]}, {'anni_ricovero': -0.2200000000000002, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.32110890232035]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.67147628555883]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.44028914602521]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [39.20910200649159]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [38.98084128644574]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.749068863014564]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.5184670073785]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.28786515174242]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [38.056092728311256]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.8278320082654]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.59664486873178]}, {'anni_ricovero': -1.29, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.365457729198155]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'prediction': [39.71582511243665]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 6.15, 'prediction': [39.48463797290302]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 5.359999999999999, 'prediction': [39.2534508333694]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 4.58, 'prediction': [39.025190113323546]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'prediction': [38.79341768989238]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 3.0, 'prediction': [38.56281583425631]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'prediction': [38.33221397862024]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 1.42, 'prediction': [38.100441555189065]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'prediction': [37.87218083514321]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'prediction': [37.640993695609595]}, {'anni_ricovero': -2.3600000000000003, 'SF12_PhysicalScore_PreOp': -0.94, 'prediction': [37.40980655607597]}], [{'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.758392348699715]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.42213956839026]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [40.083130617750385]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.74687783744093]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.41062505713146]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [39.074372276822004]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.73811949651254]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.401866716203074]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [38.06561393589361]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.72660498525374]}, {'SF12_PhysicalScore_PreOp': 6.9399999999999995, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.390352204944286]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.70370454181935]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.36745176150989]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [40.02844281087002]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.69219003056056]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.355937250251095]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [39.01968446994164]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.68343168963217]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.34717890932271]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [38.01092612901325]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.67191717837338]}, {'SF12_PhysicalScore_PreOp': 6.15, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.33566439806392]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.64901673493898]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.312763954629524]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.97375500398965]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.637502223680194]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.30124944337073]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.96499666306127]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.628743882751806]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.29249110244234]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.95623832213288]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.61722937149301]}, {'SF12_PhysicalScore_PreOp': 5.359999999999999, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.28097659118355]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.59502117877862]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.258768398469165]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.91975944782929]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.583506667519835]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.24725388721037]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.91100110690091]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.57474832659145]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.23849554628198]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.902242765972524]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.56323381533265]}, {'SF12_PhysicalScore_PreOp': 4.58, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.226981035023194]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.540194921754264]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.2039421414448]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.86493319080493]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.52868041049547]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.192427630186]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.856174849876545]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.51992206956708]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.18366928925762]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.84741650894816]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.50840755830829]}, {'SF12_PhysicalScore_PreOp': 3.7880000000000003, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.17215477799883]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.4856455650179]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.14939278470843]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.81038383406857]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.4741310537591]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.137878273449644]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.80162549314018]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.465372712830714]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.129119932521256]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.79286715221179]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.453858201571926]}, {'SF12_PhysicalScore_PreOp': 3.0, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.11760542126246]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.43109620828153]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.09484342797207]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.7558344773322]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.41958169702274]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.08332891671328]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.74707613640382]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.410823356094355]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.07457057578489]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.738317795475425]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.39930884483556]}, {'SF12_PhysicalScore_PreOp': 2.2119999999999997, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.0630560645261]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.37626995125717]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [40.040017170947706]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.701008220307834]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.364755439998376]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [39.02850265968891]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.692249879379446]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.35599709906999]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [38.01974431876052]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.683491538451065]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.34448258781119]}, {'SF12_PhysicalScore_PreOp': 1.42, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [37.008229807501735]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.32227439509681]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [39.98602161478735]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.647012664147475]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.31075988383802]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [38.97450710352855]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.63825432321909]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.30200154290962]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [37.965748762600164]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.6294959822907]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.290487031650834]}, {'SF12_PhysicalScore_PreOp': 0.6400000000000001, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [36.954234251341376]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.267586588216446]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [39.93133380790698]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.59232485726711]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.25607207695765]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [38.919819296648186]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.58356651633872]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.24731373602926]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [37.9110609557198]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.57480817541034]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.23579922477047]}, {'SF12_PhysicalScore_PreOp': -0.1499999999999999, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [36.89954644446101]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 9.11, 'prediction': [40.21289878133608]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 7.89, 'prediction': [39.876646001026614]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 6.66, 'prediction': [39.53763705038675]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 5.4399999999999995, 'prediction': [39.201384270077284]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 4.22, 'prediction': [38.86513148976782]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 3.0, 'prediction': [38.52887870945836]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 1.78, 'prediction': [38.192625929148896]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': 0.56, 'prediction': [37.85637314883944]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': -0.6600000000000001, 'prediction': [37.52012036852997]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': -1.8899999999999997, 'prediction': [37.18111141789011]}, {'SF12_PhysicalScore_PreOp': -0.94, 'SF12_MentalScore_PreOp': -3.1100000000000003, 'prediction': [36.84485863758064]}]
        ]};

window.addEventListener('load', function () {
    let dashboard = document.getElementById('results');
    dashboard.classList.add('d-none');
    let spinner = document.getElementById('spinner');
    spinner.classList.add('d-block');
    getResults();
})

// crea l''interfaccia utente per la parte del controfattuale.
// bisogna passare come parametro l'array contenente gli array con i valori dei campi del controfattuale
function createCounterfactual(counterfactData) {
    if(dataType == 'physical'){
        let isParam = document.getElementById('isPhysicalParam');
        isParam.classList.add('d-flex');
        for (let i = 0; i < 2; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            // nome del campo controfattuale in uno dei paragrafi
            if(counterfactData.physical[i][0] == 'anni_ricovero'){
                p.innerHTML = 'Età';
                for (let j = 1; j < 10; j++) {
                    if (counterfactData.physical[i][j] > 0){
                        let opt = document.createElement('option');
                        opt.value = counterfactData.physical[i][j];
                        opt.innerHTML = Math.round(counterfactData.physical[i][j]);
                        if (j == 5) {
                            opt.selected = "selected";
                        }
                        select.appendChild(opt);
                    }
                }
            } else {
                p.innerHTML = counterfactData.physical[i][0].replace('_', " ");
                for (let j = 1; j < 10; j++) {
                    if (counterfactData.physical[i][j] > 0){
                        let opt = document.createElement('option');
                        opt.value = counterfactData.physical[i][j];
                        opt.innerHTML = counterfactData.physical[i][j].toFixed(2);
                        if (j == 5) {
                            opt.selected = "selected";
                        }
                        select.appendChild(opt);
                    }
                }
            }

        }
    } else if(dataType == 'mental'){
        let isParam = document.getElementById('isMentalParam');
        isParam.classList.add('d-flex');
        for (let i = 5; i < 7; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            p.innerHTML = counterfactData.mental[i-5][0].replace('_'," ");

            for (let j = 1; j < 10; j++) {
                if (counterfactData.physical[i-5][j] > 0){
                    let opt = document.createElement('option');
                    opt.value = counterfactData.mental[i-5][j];
                    opt.innerHTML = counterfactData.mental[i-5][j];
                    if (j == 5) {
                        opt.selected = "selected";
                    }
                    select.appendChild(opt);
                }
            }
        }
    } else if(dataType == 'ODI'){
        let isParam = document.getElementById('isODIParam');
        isParam.classList.add('d-flex');
        for (let i = 5; i < 7; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            p.innerHTML = counterfactData.ODI[i-5][0].replace('_'," ");

            for (let j = 1; j < 10; j++) {
                if (counterfactData.physical[i-5][j] > 0){
                    let opt = document.createElement('option');
                    opt.value = counterfactData.ODI[i-5][j];
                    opt.innerHTML = counterfactData.ODI[i-5][j];
                    if (j == 5) {
                        opt.selected = "selected";
                    }
                    select.appendChild(opt);
                }
            }
        }
    }
}


function newResultsP(data = jsonControfact) {
    const pred_len = data.predictions[1].length;

    let p0 = document.getElementById("counterfact0p").innerHTML;
    if(p0 == 'Età'){
        p0 = 'anni_ricovero';
    }
    let select0 = document.getElementById("counterfact0sel");
    let p1 = document.getElementById("counterfact1p").innerHTML.replace(' ',"_");
    let select1 = document.getElementById("counterfact1sel");


    // scorro l'attay delle predizioni controfattuali e:
    // 1) controllo che tutti i campi del controfattuale siano nell'oggetto corrente
    // 2) controllo che il valore dei campi dell'oggetto sia uguale al valore scelto dall'utente
    // se i controlli sono superati inserisco il valore della predizione nella tabella
    for (let i = 0; i < pred_len; i++){
        if (p0 in data.predictions[1][i] && p1 in data.predictions[1][i]
            /* && p2 in data.predictions[1][i] && p3 in data.predictions[1][i] && p4 in data.predictions[1][i] */){
            if (select0.value == data.predictions[1][i][p0] && select1.value == data.predictions[1][i][p1]
                /*&& select2.value == data.predictions[1][i][p2] && select3.value == data.predictions[1][i][p3] && select4.value == data.predictions[1][i][p4]*/){
                //document.getElementById("valore1tab").innerHTML = data.predictions[1][i].prediction;
                sessionStorage.setItem('physicalValPrediction', data.predictions[1][i].prediction);
            }
        }
    }
}


function newResultsM(data = jsonControfact) {
    //const data = JSON.parse(sessionStorage.getItem('data'));
    const pred_len = data.predictions[2].length;

    let p0 = document.getElementById("counterfact5p").innerHTML;
    let select0 = document.getElementById("counterfact5sel");
    let p1 = document.getElementById("counterfact6p").innerHTML;
    let select1 = document.getElementById("counterfact6sel");

    // confronto il mio oggetto "stringhificato" con gli oggetti del controfattuale "stringhitifati"
    // e quando trovo una corrispondenza prendo il valore della predizione e lo metto nella tabella
    // dei risultati
    for (let i = 0; i < pred_len; i++){
        if (p0 in data.predictions[2][i] && p1 in data.predictions[2][i]
            /* && p2 in data.predictions[2][i] && p3 in data.predictions[2][i] && p4 in data.predictions[2][i] */){
            if (select0.value == data.predictions[2][i][p0] && select1.value == data.predictions[2][i][p1]
                /*&& select2.value == data.predictions[2][i][p2] && select3.value == data.predictions[2][i][p3] && select4.value == data.predictions[2][i][p4]*/){
                //document.getElementById("valore2tab").innerHTML = data.predictions[2][i].prediction;
                sessionStorage.setItem('mentalValPrediction', data.predictions[2][i].prediction);
            }
        }
    }
}

function getResults() {
    const data = JSON.parse(sessionStorage.getItem('dataEl'));
    createCounterfactual(data.predictionsR.counterfactual);

    /* scatter plot */
    let margin = {top: 10, right: 30, bottom: 100, left: 100},
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#scatterPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    /* aggiungere un controllo che fa visualizzare elementi nella tabella se zonaOp è settato a 2 (spine) o 0 e 1 (knee e hip)
    * così da gestire i dati che vengono visualizzati in tabella per i diversi tipi di classificazione
    * Volendo si può gestire la visualizzazione o meno di tabelle distinte a seconda del caso anche in relazione allo scoreValue */
    const zonaOp = sessionStorage.getItem('zona_operazione');
    const scoreValue = sessionStorage.getItem('score');
    /* funzione separata per organizzare il codice */
    controlloTabelle(zonaOp, scoreValue);
    let dataViz = data.predictionsR.similar_patients;
    let patientData = {
        SF12_MentalScore_6months: data.predictionsR.predictions[0].SF12_MentalScore_6months[0],
        SF12_PhysicalScore_6months: data.predictionsR.predictions[0].SF12_PhysicalScore_6months[0],
        age: data.predictionsR.predictions[0].age[0]
    };
    let objToAnalyze = [];
    if(scoreValue == 'Phisycal'){
        objToAnalyze = dataViz.slice(0,4);
        objToAnalyze.forEach(el => {
            el.isTester = 'noF';
        })
    } else {
        objToAnalyze = dataViz.slice(5,9);
        objToAnalyze.forEach(el => {
            el.isTester = 'noM';
        })
    }
    patientData.isTester = 'yes';
    objToAnalyze.push(patientData);
//               violinPlot(data);
    // Add X axis
    var x = d3.scaleLinear()
        .domain([0, 100])
        .range([ 0, width ]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 100])
        .range([ height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    var color = d3.scaleOrdinal()
        .domain(["yes", "noM", "noF" ])
        .range([ "#961A3C", "#E2A525", "#046697"])
    // Add dots
    if(scoreValue == 'Phisycal'){
        svg.append('g')
            .selectAll("dot")
            .data(objToAnalyze)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.age); } )
            .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
            .attr("r", 3)
            .style("fill", function (d) { return color(d.isTester) } )

    } else {
        svg.append('g')
            .selectAll("dot")
            .data(objToAnalyze)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.age); } )
            .attr("cy", function (d) { return y(d.SF12_MentalScore_6months); } )
            .attr("r", 3)
            .style("fill", function (d) { return color(d.isTester) } )
    }
    violinPlots(data.predictionsR.other_patients, 'period', 'score');
    plotWithBoxPlot(patientData);
    let barPosition = document.getElementById('valueBar');
    barPosition.style.left = data.predictionsC.mental_classif_score[0] * 100 + '%';
    setTimeout(function() {
        let dashboard = document.getElementById('results');
        dashboard.classList.remove('d-none');
        let spinner = document.getElementById('spinner');
        spinner.classList.add('d-none');
    }, 3000);
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}
function controlloTabelle(zonaOp, scoreValue) {
    if(zonaOp == 0 || zonaOp == 1){
        if(scoreValue == 'Phisycal'){
            /* inserire controllo su tabella per hip o knee physical */
            /* Creare le tabelle nell'html con un id associato e richiamare quell'elemento con l'id nel js e poi usare
            * classList.remove('d-none'); o classList.add('d-none');
            * a seconda che si voglia far visualizzare o meno la tabella, la classe d-none applica un display:none all'elemento*/
        } else {
            /* inserire controllo su tabella per hip o knee mental */
        }
    } else if(zonaOp == 2){

        if(scoreValue == 'Phisycal'){
            /* inserire controllo su tabella per spine phisycal */
        } else {
            /* inserire controllo su tabella per spine ODI */
        }
    } else {
        // transferFailed();
    }
}

function plotWithBoxPlot(dataset){
    let newDataset = [];
    newDataset.push(dataset);
    let margin = {top: 10, right: 10, bottom: 40, left: 40},
        width = 350 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#plotWBox")
        .append("svg")
        .style("background-color", "transparent")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    // Add X axis
    var x = d3.scaleLinear()
        .domain([0, 100])
        .range([ 0, width ]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 100])
        .range([ height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    svg.append('g')
        .selectAll("dot")
        .data(newDataset)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.SF12_MentalScore_6months); } )
        .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
        .attr("r", 3)
        .style("fill", '#BADAE9' )

    svg.append('g')
        .selectAll("dot")
        .data(newDataset)
        .enter()
        .append('circle')
        .attr("cx", function (d) { return x(d.SF12_MentalScore_6months); } )
        .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
        .attr('r', 10)
        .attr('stroke', '#BADAE9')
        .attr('fill', 'none');

// Add the path using this helper function
    svg
        .append("g")
        .selectAll("dot")
        .data(newDataset)
        .enter()
        .append("line")
        .attr("x1", function(d){return(x(d.SF12_MentalScore_6months))})
        .attr("x2", function(d){return(x(d.SF12_MentalScore_6months))})
        .attr("y1", function(d){return(y(d.SF12_PhysicalScore_6months + 10))})
        .attr("y2", function(d){return(y(d.SF12_PhysicalScore_6months - 10))})
        .attr("stroke", "#BADAE9")
        .style("width", 1)
}

function violinPlots(dataset){
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
    var svg = d3.select("#violinPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

        // Build and Show the Y scale
        var y = d3.scaleLinear()
            .domain([ 0,1 ])          // Note that here the Y scale is set manually
            .range([height, 0])
        svg.append("g").call( d3.axisLeft(y) )

        // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(["preOp", "6motnhs"])
            .padding(0.05)     // This is important: it is the space between 2 groups. 0 means no padding. 1 is the maximum.
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))

        // Features of the histogram
        var histogram = d3.histogram()
            .domain(y.domain())
            .thresholds(y.ticks(20))    // Important: how many bins approx are going to be made? It is the 'resolution' of the violin plot
            .value(d => d)

        // Compute the binning for each group of the dataset
       var sumstat = d3.nest()  // nest function allows to group the calculation per level of a factor
            .key(function(d) { return d.period;})
            .rollup(function(d) {   // For each key..
                input = d.map(function(g) { return g.score;})    // Keep the variable called Sepal_Length
                bins = histogram(input)   // And compute the binning on it.
                return(bins)
            })
            .entries(dataset);
     // What is the biggest number of value in a bin? We need it cause this value will have a width of 100% of the bandwidth.
     var maxNum = 0
     for ( i in sumstat ){
         allBins = sumstat[i].value
         lengths = allBins.map(function(a){return a.length;})
         longuest = d3.max(lengths)
         if (longuest > maxNum) { maxNum = longuest }
     }

     // The maximum width of a violin must be x.bandwidth = the width dedicated to a group
     var xNum = d3.scaleLinear()
         .range([0, x.bandwidth()])
         .domain([-maxNum,maxNum])

     // Add the shape to this svg!
     svg
         .selectAll("myViolin")
         .data(sumstat)
         .enter()        // So now we are working group per group
         .append("g")
         .attr("transform", function(d){ return("translate(" + x(d.key) +" ,0)") } ) // Translation on the right to be at the group position
         .append("path")
         .datum(function(d){ return(d.value)})     // So now we are working bin per bin
         .style("stroke", "none")
         .style("fill","#C4C4C4")
         .attr("d", d3.area()
             .x0(function(d){ return(xNum(-d.length)) } )
             .x1(function(d){ return(xNum(d.length)) } )
             .y(function(d){ return(y(d.x0)) } )
             .curve(d3.curveCatmullRom)    // This makes the line smoother to give the violin appearance. Try d3.curveStep to see the difference
         )

        // Compute quartiles, median, inter quantile range min and max --> these info are then used to draw the box.
        var sumstatBox = d3.nest() // nest function allows to group the calculation per level of a factor
            .key(function(d) { return d.period;})
            .rollup(function(d) {
                q1 = d3.quantile(d.map(function(g) { return g.score;}).sort(d3.ascending),.25)
                median = d3.quantile(d.map(function(g) { return g.score;}).sort(d3.ascending),.5)
                patient = JSON.parse(sessionStorage.getItem('dataEl')).predictionsC.mental_classif_score[0]
                q3 = d3.quantile(d.map(function(g) { return g.score;}).sort(d3.ascending),.75)
                interQuantileRange = q3 - q1
                min = q1 - 1.5 * interQuantileRange
                max = q3 + 1.5 * interQuantileRange
                return({q1: q1, median: median, patient: patient, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max})
            })
            .entries(dataset)

        // Show the X scale
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(["preOp", "6motnhs"])
            .paddingInner(10.2)
            .paddingOuter(.52)

        // Show the Y scale
        var y = d3.scaleLinear()
            .domain([0,1])
            .range([height, 0])
    svg.append("g").call(d3.axisLeft(y))

    const createGradient = select => {
        const gradient = select
            .select('defs')
            .append('linearGradient')
            .attr('id', 'gradient')
            .attr('x1', '0%')
            .attr('y1', '100%')
            .attr('x2', '0%')
            .attr('y2', '35%');

        gradient
            .append('stop')
            .attr('offset', '35%')
            .attr('style', 'stop-color:#2CB7EA;stop-opacity:1');

        gradient
            .append('stop')
            .attr('offset', '65%')
            .attr('style', 'stop-color:#E3F4FC;stop-opacity:1');

        gradient
            .append('stop')
            .attr('offset', '100%')
            .attr('style', 'stop-color:#C02026;stop-opacity:1');
    };

    svg.append('defs');
    svg.call(createGradient);
        // Show the main vertical line
    svg
            .selectAll("vertLines")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key))})
            .attr("x2", function(d){return(x(d.key))})
            .attr("y1", function(d){return(y(d.value.min))})
            .attr("y2", function(d){return(y(d.value.max))})
            .attr("stroke", "#A4A5A5")
            .style("width", 10)

        // rectangle for the main box
        var boxWidth = 20
    svg
            .selectAll("boxes")
            .data(sumstatBox)
            .enter()
            .append("rect")
            .attr("x", function(d){return(x(d.key)-boxWidth/2)})
            .attr("y", function(d){return(y(d.value.q3))})
            .attr("height", function(d){return(y(d.value.q1)-y(d.value.q3))})
            .attr("width", boxWidth )
            .attr("stroke", "white")
            .style('fill', 'url(#gradient)')

        // Show the median
    svg
            .selectAll("medianLines")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key)-boxWidth/2) })
            .attr("x2", function(d){return(x(d.key)+boxWidth/2) })
            .attr("y1", function(d){return(y(d.value.median))})
            .attr("y2", function(d){return(y(d.value.median))})
            .attr("stroke", "#CFE6F3")
            .style("width", 20)

    // Draw the whiskers at the min for this series
        svg.selectAll("indPoints")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key)-boxWidth/2) })
            .attr("x2", function(d){return(x(d.key)+boxWidth/2) })
            .attr("y1", function(d){return(y(d.value.patient))})
            .attr("y2", function(d){return(y(d.value.patient))})
            .attr("stroke", "#000")
            .attr("stroke-width", 1)
            .attr("fill", "none");
}

function evalPred(type){
    let modale = document.getElementById('evalModal');
    if(!modale.classList.contains('show')){
        modale.classList.add('show');
        modale.classList.add('d-block');
    } else {
        modale.classList.remove('d-block');
        modale.classList.remove('show');
    }
}