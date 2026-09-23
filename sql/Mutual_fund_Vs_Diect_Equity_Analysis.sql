# Mutual Fund vs Direct Equity trend analysis project

create database mutual_fund_analysis;
use mutual_fund_analysis;

-- -- -- -- -- -- -- -- -- MUTUAL FUND TABLE -- -- -- -- -- -- -- -- -- -- -- -- -- 
create table mutual_fund (
    Year int,
    Month varchar(20),
    Scheme_Name varchar(255),
    No_of_Schemes float,
    No_of_Folios float,
    Funds_Mobilized float,
    Redemption float,
    Net_Inflow float,
    AUM float,
    AAUM float
);

-- -- -- -- -- -- -- -- -- -- DIRECT EQUITY TABLE -- -- -- -- -- -- -- -- -- -- -- -- 
create table direct_equity (
    Year int,
    Month varchar(20),
    BSE_Equity_Value float,
    NSE_Equity_Value float,
    Total_Equity_Settlement_Value float
);

select * from mutual_fund;
select * from direct_equity;

select count(*) as total_records from mutual_fund;
use mutual_fund_analysis;
truncate table mutual_fund;

select count(*) as total_records from direct_equity;

-- -- -- -- -- -- -- -- Year-wise Mutual Fund AUM -- -- -- -- -- -- -- -- 
select year,avg(AUM) as average_aum from mutual_fund 
group by Year order by Year;

-- -- -- -- -- -- -- -- Year-wise Mutual Fund Net Inflow -- -- -- -- -- -- -- --
select Year,avg(Net_Inflow) as average_net_inflow from mutual_fund
group by Year order by Year;

-- -- -- -- -- -- -- -- Year-wise Direct Equity Settlement Value -- -- -- -- -- -- 
select Year,avg(Total_Equity_Settlement_Value) as average_equity_value from direct_equity
group by Year order by Year;

-- -- -- -- -- -- -- -- BSE vs NSE Average Value -- -- -- -- -- -- -- -- -- --
select avg(BSE_Equity_Value) as average_bse,avg(NSE_Equity_Value) as average_nse from direct_equity;

-- -- -- -- -- -- -- -- Year-wise Mutual Fund Folios -- -- -- -- -- -- -- -- -- 
select Year,avg(No_of_Folios) as average_folios from mutual_fund
group by Year order by Year;

-- -- -- -- -- -- -- -- Top 10 Mutual Fund Schemes by Average AUM -- -- -- -- -- -- 
select Scheme_Name,avg(AUM) as average_aum from mutual_fund
group by Scheme_Name
order by average_aum desc
limit 10;

-- -- -- -- -- -- -- -- Positive vs Negative Net Inflow -- -- -- -- -- -- -- -- -- 
select
    case
        when Net_Inflow > 0 then 'Positive'
        when Net_Inflow < 0 then 'Negative'
        else 'Zero'
    end as Inflow_Status,
    count(*) as Record_Count
from mutual_fund
group by Inflow_Status;

-- -- -- -- -- -- Mutual Fund vs Direct Equity - Year-wise Comparison -- -- -- 
select
    m.Year,avg(m.AUM) as average_mutual_fund_aum,
    avg(d.Total_Equity_Settlement_Value) as average_direct_equity_value
from mutual_fund m
inner join direct_equity d
    on m.Year = d.Year
group by m.Year
order by m.Year;

















