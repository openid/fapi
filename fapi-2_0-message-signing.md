%%%
title = "FAPI 2.0 Message Signing - Draft 02"
abbrev = "fapi-message-signing-2"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-message-signing-2_0-02"
status = "standard"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
    [author.address]
    email = "dave@tonge.org"
 
[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="Authlete"
    [author.address]
    email = "mail@danielfett.de"

[[author]]
initials="J."
surname="Heenan"
fullname="Joseph Heenan"
organization="Authlete"
    [author.address]
    email = "joseph@authlete.com"

%%%

.# Abstract

OIDF FAPI 2.0 Message Signing is an API security profile that provides interoperable 
support for non-repudiation across OAuth 2.0 [@!RFC6749] based requests and responses.

.# Foreword

The OpenID Foundation (OIDF) promotes, protects and nurtures the OpenID community and technologies. As a non-profit international standardizing body, it is comprised by over 160 participating entities (workgroup participant). The work of preparing implementer drafts and final international standards is carried out through OIDF workgroups in accordance with the OpenID Process. Participants interested in a subject for which a workgroup has been established have the right to be represented in that workgroup. International organizations, governmental and non-governmental, in liaison with OIDF, also take part in the work. OIDF collaborates closely with other standardizing bodies in the related fields.

Final drafts adopted by the Workgroup through consensus are circulated publicly for the public review for 60 days and for the OIDF members for voting. Publication as an OIDF Standard requires approval by at least 50% of the members casting a vote. There is a possibility that some of the elements of this document may be the subject to patent rights. OIDF shall not be held responsible for identifying any or all such patent rights.


.# Introduction

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This Message Signing Profile is part of the FAPI 2.0 family of specifications with a focus on providing interoperable support for non-repudiation across OAuth 2.0 based requests and responses. 

It has been formally analysed [@FAPI2MSANALYSIS] for it's security and non-repudiation properties.

.# Warning

This document is not an OIDF International Standard. It is distributed for
review and comment. It is subject to change without notice and may not be
referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and to
provide supporting documentation.

.# Notational conventions

The keywords "shall", "shall not", "should", "should not", "may", and "can" in
this document are to be interpreted as described in ISO Directive Part 2
[@ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

{mainmatter}

# Scope

This document specifies the methods for clients, authorization servers and resource servers to sign and verify messages.

# Normative references

The following documents are referred to in the text in such a way that some or all of their content constitutes requirements of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.

See Clause 8 for normative references.

# Terms and definitions

For the purpose of this document, the terms defined in [@!RFC6749], [@!RFC6750], [@!RFC7636], [@!OIDC] and [@!ISO29100] apply.

# Symbols and Abbreviated terms

**API** – Application Programming Interface

**HTTP** – Hyper Text Transfer Protocol

**JAR** – JWT-Secured Authorization Request

**JARM** – JWT Secured Authorization Response Mode

**JWT** – JSON Web Token

**JSON** – JavaScript Object Notation

**OIDF** – OpenID Foundation

**PAR** – Pushed Authorization Requests

**PKCE** – Proof Key for Code Exchange

**REST** – Representational State Transfer

**TLS** – Transport Layer Security

**URI** – Uniform Resource Identifier

**URL** – Uniform Resource Locator

# Message signing profile

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This Message Signing Profile aims to reach the security goals
laid out in the Attacker Model [@!attackermodel] plus the non-repudiation goals listed below.

All provisions of the [@!FAPI2_Security_Profile] apply to the Message Signing Profile
as well, with the extensions described in the following.


## Profile

In addition to the technologies used in the [@!FAPI2_Security_Profile], the
following standards are used in this profile:

  * OAuth 2.0 JWT Secured Authorization Request (JAR) [@!RFC9101] for signing authorization requests
  * JWT Secured Authorization Response Mode for OAuth 2.0 [@!JARM] for signing authorization responses 
  * OAuth 2.0 Token Introspection [@!RFC7662] with [@!RFC9701] for signing introspection responses

We understand that some ecosystems may only desire to implement 1, 2 or 3 of the above, it is therefore
anticipated that a piece of software will be able to conform to each of the methods separately, i.e. there
will be separate conformance testing options for each of the following:

 * Signed authorization requests
 * Signed authorization responses
 * Signed introspection responses 


## Non-repudiation

Beyond what is captured by the security goals and the attacker model in
[@!attackermodel], parties could try to deny having sent a particular message,
for example, a payment request. For this purpose, non-repudiation is needed.

In the context of this specification, non-repudiation refers to the assurance that the owner of 
a signature key pair that was capable of generating an existing signature corresponding to certain 
data cannot convincingly deny having signed the data ([@!NIST.SP.800-133]).

This is usually achieved by providing application-level signatures that can be
stored together with the payload and meaningful metadata of a request or
response. 

The following messages are affected by this specification:

  * NR1: pushed authorization requests
  * NR2: authorization requests (front-channel)
  * NR3: authorization responses (front-channel)  
  * NR4: introspection responses  
  * NR5: ID tokens

## Signing authorization requests

To support non-repudiation for NR1, pushed authorization requests can be signed. 
Because FAPI2 uses [@!RFC9126], NR2 is achieved by default when the pushed authorization request
is signed.


### Requirements for authorization servers

Authorization servers implementing FAPI2 authorization request signing

 1. shall support, require use of, and verify signed request objects according to JAR
    [@!RFC9101] at the PAR endpoint [@!RFC9126];
 2. shall require the aud claim in the request object to be, or to be an array containing, the authorization server's issuer identifier URL;
 3. shall require the request object to contain an `nbf` claim that is no longer than 60 minutes in the past; and
 4. shall require the request object to contain an `exp` claim that has a lifetime of no longer than 60 minutes after the `nbf` claim;
 5. shall accept request objects with `typ` header parameter with a value `oauth-authz-req+jwt`.

### Requirements for clients

Clients implementing FAPI2 authorization request signing

 1. shall send all authorization parameters to the PAR endpoint [@!RFC9126] in a JAR
    [@!RFC9101] signed requested object;
 2. shall send the `aud` claim in the request object as the authorization server's issuer identifier URL;
 3. shall send a `nbf` claim in the request object;
 4. shall send an `exp` claim in the request object that has a lifetime of no longer than 60 minutes;
 5. should send a `typ` header parameter with a value `oauth-authz-req+jwt`.

### Client metadata {#client-metadata}

The Dynamic Client Registration Protocol [@RFC7591] defines an API
for dynamically registering OAuth 2.0 client metadata with authorization servers.
The metadata defined by [@RFC7591], and registered extensions to it,
also imply a general data model for clients that is useful for authorization server implementations
even when the dynamic client registration protocol isn't in play.
Such implementations will typically have some sort of user interface available for managing client configuration.

The following client metadata parameter is introduced by this specification:

* `response_modes`: 
    * OPTIONAL. A JSON array of strings containing the list of response modes that
      the client may use. If omitted, the default is that the client may use any of
      the response modes supported by the authorization server.
 
## Signing authorization responses

To support non-repudiation for NR3, authorization responses can be signed. 

### Requirements for authorization servers

Authorization servers implementing FAPI2 authorization response signing

 1. shall support, require use of, and issue signed authorization responses via JWT Secured Authorization 
    Response Mode for OAuth 2.0 [@!JARM].

**NOTE**: When using [@!JARM] an authorization server should only include the iss authorization response 
parameter defined by [@!RFC9207] inside the JWT. This is because [@!RFC9207] defines `iss` 
to be an authorization response parameter, and [@!JARM] Section 4.1 requires all authorization 
response parameters to be inside the JWT.

### Requirements for clients

Clients implementing FAPI2 authorization response signing

 1. shall set the `response_mode` to `jwt` in the authorization request as defined in [@!JARM]; and
 2. shall verify signed authorization responses according to [@!JARM].


## Signing introspection responses

To support non-repudiation for NR4, introspection responses can be signed.

### Requirements for authorization servers

Authorization servers implementing FAPI2 introspection response signing

 1. shall sign introspection responses that are issued in JWT format according to [@!RFC9701]
 
### Requirements for clients

Clients implementing FAPI2 introspection response signing

 1. shall request signed token introspection responses according to [@!RFC9701]; and
 2. shall verify the signed token introspection responses.

## Signing ID tokens

To support non-repudiation for NR5, signed ID tokens are used.

### Requirements for authorization servers

No additional requirements. 

Note: Authorization servers implementing FAPI2 are already required to sign ID tokens as specified in section 5.4.1 in the [@!FAPI2_Security_Profile].
 
### Requirements for clients

Clients requesting and receiving ID tokens

1. shall verify the signature of the signed ID token received.
 
# Security considerations

## Authorization response encryption

In FAPI2, there is no confidential information in the authorization response, hence encryption of the authorization response is not required for the purposes of security or confidentiality. In addition, to achieve greater interoperability, it is not recommended to use encryption in this case. 

Usage of PKCE in FAPI 2 provides protection for code leakage described in Section 5.4 of [@!JARM].

## Confusion between resource servers and clients in introspection request

In [@!RFC9701], the resource server accessing
the introspection endpoint is seen in the role of a client towards the
authorization server that is providing the introspection endpoint. A malicious
client (that is not a resource server) could attempt to call the introspection
endpoint directly, and thus gather information about an access token to which it
is not supposed to have access. This may, for example, leak secrets including,
if the access token was leaked or stolen, personal information about an
end-user.

The authorization server therefore must ensure that the resource server is not
confused with a regular client that is not supposed to call the introspection
endpoint, and that the resource server has the necessary authorization to access
the information associated with the access token.

## Non-repudiation limited to individual messages

It is important to note that while this specification provides mechanisms for non-repudiation for 
individual messages, it does not provide non-repudiation guarantees for a sequence of messages.

## Non-repudiation not provided for front channel authorization requests

While only a small amount of information is present in a [@!FAPI2_Security_Profile] front channel 
authorization request, it is important to note that non-repudiation is not provided for this message. 

## Difficulty in linking a signed message to a real world identity

This specification provides the technical means to sign messages, however proving that a specific signed response is
linked to a specific real world end-user, or that a real world end-user initiated a specific request is outside of the
scope of this document.

## The value of JARM for non-repudiation

The values signed in a JARM response may be of limited value for non-repudiation as the values are artifacts 
of the OAuth flow (e.g. code and state) rather than real world values (e.g. account number and amount). However JARM
is still useful in providing message integrity to the authorization response.



# Privacy considerations

In addition to the privacy considerations detailed in [@!FAPI2_Security_Profile] implementers should consider
the privacy implications of storing messages for the purpose of non-repudiation. 

Such messages may well contain personally identifiable information and implementers should evaluate 
whether such messages need to be stored. If they are stored then adequate access controls must be 
put in place to protect that data. Such controls should follow data minimisation principles and ensure that 
there are tamper-proof audit logs.

# IANA considerations
## OAuth dynamic client registration metadata registration

This specification requests registration of the following client metadata
definitions in the IANA "OAuth Dynamic Client Registration Metadata" registry
established by [@RFC7591]:

### Registry contents

* Client Metadata Name: `response_modes`
* Client Metadata Description: Array of the response modes that the client may use
* Change Controller: IESG
* Specification Document(s): (#client-metadata) of this specification

# Acknowledgements

This specification was developed by the OpenID FAPI Working Group. 

We would like to thank Takahiko Kawasaki, Filip Skokan, Nat Sakimura, Dima Postnikov, Brian Campbell, Ralph Bragg, Justin Richer and Lukasz Jaromin for their valuable feedback and contributions that helped to evolve this specification.


{backmatter}

<reference anchor="FAPI2_Security_Profile" target="https://openid.net/specs/fapi-security-profile-2_0.html">
  <front>
    <title>FAPI 2.0 Security Profile</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
    <author initials="D." surname="Tonge" fullname="Dave Tonge">
      <organization>Moneyhub Financial Technology Ltd.</organization>
    </author>
    <author initials="J." surname="Heenan" fullname="Joseph Heenan">
      <organization>Authlete</organization>
    </author>
   <date day="22" month="Feb" year="2025"/>
  </front>
</reference>

<reference anchor="attackermodel" target="https://openid.net/specs/fapi-attacker-model-2_0.html">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="22" month="FEb" year="2025"/>
  </front>
</reference>

<reference anchor="OIDC" target="http://openid.net/specs/openid-connect-core-1_0.html">
  <front>
    <title>OpenID Connect Core 1.0 incorporating errata set 2</title>
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

<reference anchor="JARM" target="https://openid.net/specs/oauth-v2-jarm-final.html">
  <front>
    <title>JWT Secured Authorization Response Mode for OAuth 2.0 (JARM)</title>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt">
      <organization>Yes</organization>
    </author>
    <author initials="B." surname="Campbell" fullname="Brian Campbell">
      <organization>Ping</organization>
    </author>
   <date day="9" month="Nov" year="2022"/>
  </front>
</reference>

<reference anchor="FAPI2MSANALYSIS" target="http://dx.doi.org/10.18419/opus-13698">
  <front>
    <title>Formal security analysis of the OpenID FAPI 2.0 Security Profile with 
    FAPI 2.0 Message Signing, FAPI-CIBA, Dynamic Client Registration and Management </title>    
    <author initials="P." surname="Hosseyni" fullname="Pedram Hosseyni">
      <organization>University of Stuttgart, Germany</organization>
    </author>
    <author initials="R." surname="Kuesters" fullname="Ralf Kuesters">
      <organization>University of Stuttgart, Germany</organization>
    </author>
    <author initials="T." surname="Würtele" fullname="Tim Würtele">
      <organization>University of Stuttgart, Germany</organization>
    </author>
    <date day="04" month="Oct" year="2024"/>
  </front>  
</reference>

<reference anchor="NIST.SP.800-133" target="https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-133.pdf">
  <front>
    <title>NIST Special Publication 800-133</title>
     <author fullname="Elaine Barker">
      <organization></organization>
    </author>
     <author fullname="Allen Roginsky ">
      <organization></organization>
    </author>
   <date day="23" month="July" year="2019"/>
  </front>
</reference>



<reference anchor="ISODIR2" target="https://www.iso.org/sites/directives/current/part2/index.xhtml">
<front>
<title>ISO/IEC Directives, Part 2 - Principles and rules for the structure and drafting of ISO and IEC documents</title>
    <author fullname="ISO/IEC">
      <organization>ISO/IEC</organization>
    </author>
</front>
</reference>


<reference anchor="ISO29100" target="https://standards.iso.org/ittf/PubliclyAvailableStandards/index.html#:~:text=IEC%2029100%3A2011-,EN,-%2D%20FR">
<front>
<title>ISO/IEC 29100 Information technology – Security techniques – Privacy framework</title>
    <author fullname="ISO/IEC">
      <organization></organization>
    </author>
</front>
</reference>

# Notices

Copyright (c) 2025 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer,
or other interested party a non-exclusive, royalty free, worldwide copyright license to
reproduce, prepare derivative works from, distribute, perform and display, this
Implementers Draft, Final Specification, or Final Specification Incorporating Errata
Corrections solely for the purposes of (i) developing specifications, and (ii)
implementing Implementers Drafts, Final Specifications, and Final Specification
Incorporating Errata Corrections based on such documents, provided that attribution
be made to the OIDF as the source of the material, but that such attribution does not
indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions
from various sources, including members of the OpenID Foundation and others.
Although the OpenID Foundation has taken steps to help ensure that the technology
is available for distribution, it takes no position regarding the validity or scope of any
intellectual property or other rights that might be claimed to pertain to the
implementation or use of the technology described in this specification or the extent
to which any license under such rights might or might not be available; neither does it
represent that it has made any independent effort to identify any such rights. The
OpenID Foundation and the contributors to this specification make no (and hereby
expressly disclaim any) warranties (express, implied, or otherwise), including implied
warranties of merchantability, non-infringement, fitness for a particular purpose, or
title, related to this specification, and the entire risk as to implementing this
specification is assumed by the implementer. The OpenID Intellectual Property
Rights policy (found at openid.net) requires contributors to offer a patent promise not
to assert certain patent claims against other contributors and against implementers.
OpenID invites any interested party to bring to its attention any copyrights, patents,
patent applications, or other proprietary rights that may cover technology that may be
required to practice this specification.

# Document History

[[ To be removed from the final specification ]]

-02
 * Update references to final versions of fapi2 security profile and message signing
 * editorial changes to get ready for final vote

-01

 * Update RFC9701 reference
 * fix merge issue
 * initial work on creating separate http signing spec
 * get rid of [[ this specification ]] brackets
 * numbering corrected and reworded the requirement
 * Minor clarifications and typos
 * ID token signing
 * update refs to RFCs for http signatures
 * typ in request objects
 * Fixes #653 - Update abbreviated terms
 * Addresses #672 - inconsistent capitalization
 * Add Joseph to the FAPI2 SP & MS authors list
 * Fixes #649 - ISO29100 and ISO29134 is not in the reference
 * Add myself to the FAPI2 SP & MS authors list
 * Fixes #648 - The first paragraph of the Normative reference shall be as provided in ISODIR2
 * Fixes #645 - Author name of Normative reference ISODIR2 is wrong
 * Fixes #645 - Author name of Normative reference ISODIR2 is wrong
 * Fixes #648 - The first paragraph of the Normative reference shall be as provided in ISODIR2
 * Renumber attackers, fix editorial stuff
 * add security considerations around non repudiation limitations
 * move MTLS Protection of all endpoints to SP
 * Update DPoP references in FAPI 2 SP
 * Update http signing intro text
 * make clear that requests and responses can be signed independently
 * Incorporate Brian's feedback
 * Merged master into danielfett/fix-617
 * attempt at clarifying request-response binding
 * Fix typo
 * Proposal to fix Issue #617
 * Update affiliation to Authlete, add Dave as editor on the Security Profile, list Dave first for the Message Signing document
 * FAPI2MS: Change 'above 3' to 'above 4'
 * fapi2ms: require use of jarm, require use of jar, define response modes client metadata
 * Add copyright notice to fapi-ms
 * add draft to fapi2 message signing
 * initial work on privacy for message signing
 * FAPI2MS: Removed unused references
 * FAPI2MS: Defer http signing to next implementer's draft
 * Editorial fixes, working group in acknowledgements
 * FAPI2MS: security profile/attacker model links updated
 * add intro and rework initial section for message signing
 * use ticks so it doesn't end up as privatekeyjwt - fapi-2_0-message-signing.md edited online with Bitbucket
 * Update JARM ref in message signing
 * FAPI2MS: Create acknowledgements section
 * FAPI2MS: Make security considerations a top level section
 * FAPI2MS: Make [security profile] a real reference
 * FAPI2MS: Reword section about testing
 * FAPI2MS: Reword section about testing
 * FAPI2MS: Make [security profile] a real reference
 * Remove Dave from acknowledgements as he's an author
 * Update JARM ref in message signing
 * FAPI2MS: Make security considerations a top level section
 * FAPI2MS: Create acknowledgements section
 * FAPI2MS: Make normative references normative
 * use ticks so it doesn't end up as privatekeyjwt - fapi-2_0-message-signing.md edited online with Bitbucket
 * Update filenames

 -00

 * improvements to http sig wording
 * Improve description of attacker model
 * FAPI2MsgSign: Fix various links to the httpbis drafts
 * Change name of Advanced Profile to Message Signing