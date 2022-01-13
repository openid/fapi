%%%
title = "Financial-grade API: HTTP Signing Requirements"
abbrev = "fapi-http-signing-requirements"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "fapi", "http-signing"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-http-signing-requirements-01"
status = "standard"

[[author]]
initials="J."
surname="Heenan"
fullname="Joseph Heenan"
organization="Authlete"
role="editor"

%%%

.# Abstract

The Financial-grade API Standard provides a profile for OAuth 2.0 suitable for use in financial services and other similar higher risk scenarios. Ecosystems that have Financial-grade APIs often also have a requirement for the signing of HTTP requests or responses, this document covers the likely requirements and potential solutions.

{mainmatter}

# Introduction

## Warning

This document is not an OIDF International Standard. It is distributed for review and comment. It is subject to change without notice and may not be referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments, notification of any relevant patent rights of which they are aware and to provide supporting documentation.

## Copyright notice

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.

## Notational Conventions

The keywords "shall", "shall not", "should", "should not", "may", and 
"can" in this document are to be interpreted as described in ISO Directive Part 2 [@!ISODIR2].
These keywords are not used as dictionary terms such that any occurrence of them shall be interpreted as keywords
and are not to be interpreted with their natural language meanings.

# Financial-grade API: HTTP Signing Requirements

## Introduction

The Financial-grade API Standard provides a profile for OAuth 2.0 suitable for use in financial services and other similar higher risk scenarios. Ecosystems that have Financial-grade APIs often also have a requirement for the signing of HTTP requests or responses, this document covers the likely requirements and potential solutions.

## Scope

This document specifies the method for an application to:

* obtain OAuth tokens via a backchannel authentication flow in an appropriately secure manner for financial data access and other similar situations where the risk is higher;
* use tokens to interact with protected data via REST endpoints.

## Terms and definitions

For the purpose of this standard, the terms defined in [@!RFC6749], [@!RFC6750], [@!RFC7636], [@!OpenID] and OpenID Connect Client Initiated Backchannel Authentication Core apply.

## Symbols and Abbreviated terms

**API** – Application Programming Interface

**FAPI** - Financial-grade API

**HTTP** – Hyper Text Transfer Protocol

**OIDF** - OpenID Foundation

**REST** – Representational State Transfer

**TLS** – Transport Layer Security

## Typical requirements

### Introduction 

The section lists the likely requirements that influence the choice of HTTP signing method for ecosystems using Financial-grade APIs.

### Non-repudiation

Generally ecosystems look to signing as a method for non-repudiation, meaning that the request or response can be retained by the parties and later used as prove that the message came from a party that had possession of the relevant private key.

Although TLS certificates can be used for instantaneous proof of key possesion, it is essentially impractical to retain all the necessary state such that it is possible to later independently verify key possession.

Any signing scheme must support straightforward serialization for later verification.

### JSON payloads

As the primary use-case for Financial-grade APIs is with JSON payloads, it is generally possible to make using of signing methods that are specific to JSON.

### Interference with payload

As Financial-grade APIs always use end-to-end encrypted TLS, it is generally possible to assume that the message body will not be tampered with (deliberately or accidentally) during transport.

However many middleware systems come with REST clients that will often parse JSON payloads automatically, making it difficult to reconstruct the original message body to verify the signature. It is often possible to workaround this (for example canonicalisation or base64 encoding of payloads), but the workarounds can reduce simplicity or robustness. It is often possible to access the raw payload by avoiding use of the REST client. In time this would be less of an issue, as the hope is that REST clients would implement support for widely used signature schemes.

### Signing of entire message

In REST-like systems, the Request-URI, method and some HTTP headers often include important information that must be within the scope of the signature.


### Interoperability

HTTP signing methods must be sufficiently well specified and straightforward to implement such that the signing library does not need to be aware of ecosystem specifics.

Systems must not have high rates of false negatives between difference implementations.

## Security Considerations

There are no additional security considerations beyond those in [@!FAPI1-PART1], [@!FAPI1-PART2], [@!FAPICIBA].

## Privacy Considerations

There are no additional privacy considerations beyond those in [@!FAPI1-PART1], [@!FAPI1-PART2], [@!FAPICIBA].

## Acknowledgements

The following people contributed heavily towards this document:

* Nat Sakimura (Nomura Research Institute) -- Chair, Editor
* Anoop Saxana (Intuit) -- Co-chair, FS-ISAC Liaison
* Anthony Nadalin (Microsoft) -- Co-chair, SC 27 Liaison
* Dave Tonge (Moneyhub) -- Co-chair, UK Implementation Entity Liaison
* Brian Campbell (Ping Identity)
* John Bradley (Yubico)
* Joseph Heenan (Authlete)

{backmatter}

<reference anchor="OpenID" target="http://openid.net/specs/openid-connect-core-1_0.html">
  <front>
    <title>OpenID Connect Core 1.0 incorporating errata set 1</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="M." surname="Jones" fullname="Mike Jones">
      <organization>Microsoft</organization>
    </author>
    <author initials="B." surname="de Medeiros" fullname="Breno de Medeiros">
      <organization>Google</organization>
    </author>
    <author initials="C." surname="Mortimore" fullname="Chuck Mortimore">
      <organization>Salesforce</organization>
    </author>
   <date day="8" month="Nov" year="2014"/>
  </front>
</reference>

<reference anchor="FAPICIBA" target="https://openid.net/specs/openid-financial-api-ciba-ID1.html">
  <front>
    <title>Financial-grade API: Client Initiated Backchannel Authentication Profile</title>
    <author initials="D." surname="Tonge" fullname="Dave Tonge">
      <organization>Moneyhub</organization>
    </author>
    <author initials="J." surname="Heenan" fullname="Joseph Heenan">
      <organization>Moneyhub</organization>
    </author>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt">
      <organization>YES</organization>
    </author>
    <author initials="B." surname="Campbell" fullname="Brian Campbell">
      <organization>Google</organization>
    </author>
   <date day="15" month="Aug" year="2019"/>
  </front>
</reference>

<reference anchor="FAPI1-PART1" target="https://openid.net/specs/openid-financial-api-part-1-1_0.html">
  <front>
    <title>Financial-grade API Security Profile 1.0 - Part 1: Baseline</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="I." surname="Illumila" fullname="Illumila">
      <organization>Illumila</organization>
    </author>
   <date day="12" month="Mar" year="2014"/>
  </front>
</reference>

<reference anchor="FAPI1-PART2" target="https://openid.net/specs/openid-financial-api-part-2-1_0.html">
  <front>
    <title>Financial-grade API Security Profile 1.0 - Part 2: Advanced</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="I." surname="Illumila" fullname="Illumila">
      <organization>Illumila</organization>
    </author>
   <date day="12" month="Mar" year="2014"/>
  </front>
</reference>

<reference anchor="ISODIR2" target="https://www.iso.org/sites/directives/current/part2/index.xhtml">
<front>
<title>ISO/IEC Directives Part 2 - </title>
    <author fullname="International Organization for Standardization">
      <organization></organization>
    </author>
</front>
</reference>


